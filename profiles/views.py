from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.forms import HiddenInput
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotAllowed, HttpResponse
from django.views.generic import View, UpdateView, CreateView, DeleteView, FormView
from django.shortcuts import redirect, render

from braces.views import PermissionRequiredMixin
from social.apps.django_app.default.models import UserSocialAuth
from extra_views import ModelFormSetView

from core.utils import now, current_semester, get_default_num_shifts, get_default_num_tours, delta_semester, dues_required, parse_year_semester
from core.views import BoardOnlyMixin
from profiles.models import Person, OverrideRequirement, InactiveSemester, DuesPayment
from profiles.forms import PersonForm, SpecialRequirementsForm, PersonBulkForm, DuesPaymentForm
from profiles.utils import set_groups_by_position, member_latest_semester, send_requirements_email


class EditPersonView(PermissionRequiredMixin, BoardOnlyMixin, UpdateView):
    permission_required = 'profiles.change_person'
    model = Person
    form_class = PersonForm
    template_name = 'profiles/person_form.html'

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()

        # only superusers can change site_admin status
        try:
            obj = Person.objects.get(pk=kwargs.get('pk'))
            if not request.user.is_superuser:
                if obj.site_admin != request.POST.get('site_admin'):
                    request.POST['site_admin'] = obj.site_admin
        except Person.DoesNotExist:
            pass

        return super(EditPersonView, self).post(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(EditPersonView, self).get_form(form_class)
        if not self.request.user.person.site_admin:
            form.fields['site_admin'].widget = HiddenInput()

        form.data = form.data.copy()
        try:
            phone = form.data['phone']
            # add the '+1' if necessary
            if phone[0] != '+':
                phone = u'+1{}'.format(phone)

            form.data['phone'] = phone
        except:
            pass
        return form

    def get_context_data(self, **kwargs):
        context = super(EditPersonView, self).get_context_data(**kwargs)
        semester = current_semester()
        year = now().year
        initial_data = {'semester': semester, 'year': year, 'person': self.object}
        try:
            override_req = OverrideRequirement.objects.get(semester=semester, year=year, person=self.object)
            initial_data['tours_required'] = override_req.tours_required
            initial_data['shifts_required'] = override_req.shifts_required
        except OverrideRequirement.DoesNotExist:
            pass
        context['special_requirements_form'] = SpecialRequirementsForm(initial_data)
        context['semester'] = semester
        context['year'] = year
        return context

    def form_valid(self, form):
        form.save()

        social_auth = UserSocialAuth.objects.get(user=self.object.user)

        # create user and social auth objects
        username = self.object.harvard_email.split('@')[0]
        user = self.object.user
        user.username = username
        user.first_name = self.object.first_name
        user.last_name = self.object.last_name
        user.email = self.object.harvard_email
        user.save()

        social_auth.uid = self.object.harvard_email
        social_auth.save()

        # set appropriate groups based on position
        set_groups_by_position(self.object)

        if self.object.site_admin is True:
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()

        return super(EditPersonView, self).form_valid(form)

    def get_success_url(self):
        year, semester = member_latest_semester(self.object)
        return reverse_lazy('profiles:roster', kwargs={'year': year, 'semester': semester})


class CreatePersonView(PermissionRequiredMixin, BoardOnlyMixin, CreateView):
    permission_required = 'profiles.add_person'
    model = Person
    form_class = PersonForm
    template_name = 'profiles/person_form.html'

    def get_form(self, form_class):
        form = super(CreatePersonView, self).get_form(form_class)
        if not self.request.user.person.site_admin:
            form.fields['site_admin'].widget = HiddenInput()

        form.data = form.data.copy()
        try:
            phone = form.data['phone']
            # add the '+1' if necessary
            if phone[0] != '+':
                phone = u'+1{}'.format(phone)

            form.data['phone'] = phone
        except:
            pass

        if form.data.get('site_admin') == 'True' and not self.request.user.person.site_admin:
            form.data['site_admin'] = 'False'

        return form

    def form_valid(self, form):
        form.save()

        person = form.instance

        # create user and social auth objects
        username = person.harvard_email.split('@')[0]
        user = User.objects.create_user(username=username, email=person.harvard_email, first_name=person.first_name, last_name=person.last_name)

        # no need for the user to have a password, since we'll use Google OAuth to login
        user.set_unusable_password()
        user.save()

        person.user = user
        person.save()

        UserSocialAuth.objects.create(user=user, provider='google-oauth2', uid=person.harvard_email)

        # set appropriate groups and status based on position
        set_groups_by_position(person)

        if person.site_admin is True:
            user.is_staff = True
            user.is_superuser = True
            user.save()

        return super(CreatePersonView, self).form_valid(form)

    def get_success_url(self):
        year, semester = member_latest_semester(self.object)
        return reverse_lazy('profiles:roster', kwargs={'year': year, 'semester': semester})


class DeletePersonView(PermissionRequiredMixin, BoardOnlyMixin, DeleteView):
    permission_required = 'profiles.delete_person'
    model = Person
    form = PersonForm

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        UserSocialAuth.objects.filter(user=user).delete()
        user.delete()

        return super(DeletePersonView, self).delete(self, request, *args, **kwargs)

    def get_success_url(self):
        year, semester = member_latest_semester(self.object)
        return reverse_lazy('profiles:roster', kwargs={'year': year, 'semester': semester})


class UpdateSpecialRequirementsView(PermissionRequiredMixin, BoardOnlyMixin, FormView):
    """
    Processes updating special requirements from the edit person page
    Only allows POST
    """
    permission_required = 'profiles.add_overriderequirement'
    form_class = SpecialRequirementsForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def form_valid(self, form):
        person = form.cleaned_data.get('person')
        year = form.cleaned_data.get('year')
        semester = form.cleaned_data.get('semester')
        tours_required = form.cleaned_data.get('tours_required')
        shifts_required = form.cleaned_data.get('shifts_required')

        defaults = {
            'tours_required': tours_required,
            'shifts_required': shifts_required,
        }

        tours_required_default = get_default_num_tours()
        shifts_required_default = get_default_num_shifts()

        if tours_required is None:
            defaults['tours_required'] = tours_required_default

        if shifts_required is None:
            defaults['shifts_required'] = shifts_required_default

        if tours_required is None and shifts_required is None:
            try:
                obj = OverrideRequirement.objects.get(year=year, semester=semester, person=person)
                obj.delete()
            except OverrideRequirement.DoesNotExist:
                pass
        else:
            OverrideRequirement.objects.update_or_create(year=year, semester=semester, person=person, defaults=defaults)

        return redirect('profiles:person-edit', pk=person.pk)

    def form_invalid(self, form):
        try:
            person = form.cleaned_data.get('person')
            pk = person.pk
        except:
            raise Http404
        return redirect('profiles:person-edit', pk=pk)


class CreateInactiveSemesterView(PermissionRequiredMixin, BoardOnlyMixin, View):
    """
    Processes updating inactive semesters from the edit person page
    Only allows POST
    """
    permission_required = 'profiles.add_inactivesemester'

    def post(self, request, *args, **kwargs):
        try:
            person_pk = kwargs.get('pk')
            person = Person.objects.get(pk=person_pk)
        except:
            raise Http404

        i = 0
        semester_forms = []
        while request.POST.get('semester_{}_semester'.format(i), False):
            semester_forms.append({'semester': request.POST.get('semester_{}_semester'.format(i), None), 'year': request.POST.get('semester_{}_year'.format(i), None)})
            i += 1

        for semester_form in semester_forms:
            try:
                year = int(semester_form['year'])
                semester = semester_form['semester']

                if year is None or semester is None:
                    raise

                if not semester in ('fall', 'spring'):
                    raise

                InactiveSemester.objects.get_or_create(semester=semester, year=year, person=person)
            except:
                # form is invalid, skip
                pass

        return redirect('profiles:person-edit', pk=person_pk)


class DeleteInactiveSemesterView(PermissionRequiredMixin, BoardOnlyMixin, DeleteView):
    permission_required = 'profiles.delete_inactivesemester'
    model = InactiveSemester

    def get_success_url(self):
        return reverse_lazy('profiles:person-edit', kwargs={'pk': self.object.person.pk})


class BulkCreatePersonView(PermissionRequiredMixin, BoardOnlyMixin, ModelFormSetView):
    permission_required = 'profiles.add_person'

    model = Person
    form_class = PersonBulkForm
    template_name = 'profiles/new_person_formset.html'
    initial = []
    extra = 40
    success_url = reverse_lazy('profiles:roster-noargs')

    def construct_formset(self):
        formset = super(BulkCreatePersonView, self).construct_formset()
        formset.data = formset.data.copy()
        for key in formset.data:
            if 'phone' in key:
                try:
                    phone = formset.data[key]
                    # add the '+1' if necessary
                    if phone[0] != '+':
                        phone = u'+1{}'.format(phone)

                    formset.data[key] = phone
                except:
                    pass

        return formset

    def get_queryset(self, *args, **kwargs):
        return Person.objects.none()


class RosterView(BoardOnlyMixin, View):
    template_name = 'profiles/roster.html'

    def get_people(self, semester, year, prefetch=True):
        people = Person.objects.select_related().current_members(semester=semester, year=year).order_by('year', 'last_name', 'first_name')

        if prefetch is True:
            return people.prefetch_related('shifts', 'tours', 'overridden_requirements')
        else:
            return people

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        semester = kwargs.get('semester')

        year, semester = parse_year_semester(year=year, semester=semester)

        prev_semester = delta_semester(semester=semester, year=year, delta=-1, as_dict=True)
        next_semester = delta_semester(semester=semester, year=year, delta=1, as_dict=True)
        collect_dues = dues_required(semester=semester, year=year)

        people = self.get_people(semester=semester, year=year)

        is_current_semester = semester == current_semester() and year == now().year

        # cache requirements status results so that we don't have to keep hitting the db
        for person in people:
            dues_status = person.dues_status(semester=semester, year=year)
            person.cached_status = {
                'tours_status': person.tours_status(semester=semester, year=year),
                'shifts_status': person.shifts_status(semester=semester, year=year),
                'dues_status': dues_status,
            }

            # dues payments
            if collect_dues:
                paid = dues_status == 'complete'
                person.dues_payment_form = DuesPaymentForm(initial={'pk': person.pk, 'paid': paid}, prefix='pk_{}'.format(person.pk))

        context = {
            'semester': semester,
            'year': year,
            'people': people,
            'prev_semester': prev_semester,
            'next_semester': next_semester,
            'collect_dues': collect_dues,
            'is_current_semester': is_current_semester,
        }

        return render(request, 'profiles/roster.html', context)

    def post(self, request, *args, **kwargs):
        year = kwargs.get('year')
        semester = kwargs.get('semester')

        year, semester = parse_year_semester(year=year, semester=semester)
        people = self.get_people(semester=semester, year=year)

        if not request.user.has_perm('profiles.add_duespayment') or not request.user.has_perm('profiles.delete_duespayment') or not request.user.has_perm('profiles.change_duespayment'):
            raise PermissionDenied

        to_be_saved = []

        for person in people:
            paid = request.POST.get('pk_{}-paid'.format(person.pk), False)
            current_dues_payments = person.dues_payments.filter(semester=semester, year=year)

            if current_dues_payments and paid is False:
                current_dues_payments.delete()
            elif not current_dues_payments and paid == 'on':
                to_be_saved.append(DuesPayment(person=person, semester=semester, year=year))

        if to_be_saved:
            DuesPayment.objects.bulk_create(to_be_saved)

        return redirect('profiles:roster', semester=semester, year=year)


class RosterVCardView(BoardOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        semester = kwargs.get('semester')
        year = kwargs.get('year')
        year, semester = parse_year_semester(year=year, semester=semester)
        people = Person.objects.current_members(semester=semester, year=year)
        output = '\n'.join(person.as_vcard() for person in people)
        response = HttpResponse(output, content_type="text/x-vCard")
        response['Content-Disposition'] = 'attachment; filename=cks_members_{}_{}.vcf'.format(semester, year)

        return response


class SendRequirementsEmailsView(PermissionRequiredMixin, BoardOnlyMixin, View):
    permission_required = 'profiles.send_requirements_email'

    def post(self, request, *args, **kwargs):
        active_members = Person.objects.select_related().current_members().active()
        for person in active_members:
            send_requirements_email.delay(person)

        return render(request, 'profiles/requirements_emails_confirm.html', {'num': active_members.count()})
