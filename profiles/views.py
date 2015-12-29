from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotAllowed
from django.views.generic import View, UpdateView, CreateView, DeleteView, FormView
from django.shortcuts import redirect

from braces.views import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    GroupRequiredMixin,
)
from social.apps.django_app.default.models import UserSocialAuth

from core.utils import now, current_semester, get_default_num_shifts, get_default_num_tours
from profiles.models import Person, OverrideRequirement, InactiveSemester
from profiles.forms import PersonForm, SpecialRequirementsForm
from profiles.utils import set_groups_by_position, member_latest_semester


class EditPersonView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    permission_required = 'profiles.change_person'
    group_required = 'Board Members'
    model = Person
    form_class = PersonForm
    template_name = 'profiles/edit_person.html'

    def get_context_data(self, **kwargs):
        context = super(EditPersonView, self).get_context_data(**kwargs)
        semester = current_semester()
        year = now().year
        initial_data = {'semester': semester, 'year': year, 'person': self.object}
        try:
            override_req = OverrideRequirement.objects.filter(semester=semester, year=year, person=self.object)
            initial_data['tours_required'] = override_req.tours_required
            initial_data['shifts_required'] = override_req.shifts_required
        except OverrideRequirement.DoesNotExist:
            pass
        context['special_requirements_form'] = SpecialRequirementsForm(initial_data)
        return context

    def get_success_url(self):
        year, semester = member_latest_semester(self.object)
        return reverse_lazy('profiles:roster', kwargs={'year': year, 'semester': semester})


class CreatePersonView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    permission_required = 'profiles.add_person'
    group_required = 'Board Members'
    model = Person
    form_class = PersonForm
    template_name = 'profiles/person_form.html'

    def form_valid(self, form):
        ret = super(CreatePersonView, self).form_valid(form)

        # create user and social auth objects
        username = self.object.harvard_email.split('@')[0]
        user = User.objects.create_user(username=username, email=self.object.harvard_email, first_name=self.object.first_name, last_name=self.object.last_name)
        self.object.user = user
        self.object.save()

        UserSocialAuth.objects.create(user=user, provider='google-oauth2', uid=self.object.harvard_email)

        # set appropraite groups based on position
        set_groups_by_position(self.object)

        if self.object.site_admin is True:
            user.is_staff = True
            user.is_superuser = True
            user.save()

        return ret

    def get_success_url(self):
        year, semester = member_latest_semester(self.object)
        return reverse_lazy('profiles:roster', kwargs={'year': year, 'semester': semester})


class DeletePersonView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    permission_required = 'profiles.delete_person'
    group_required = 'Board Members'
    model = Person
    form = PersonForm

    def get_success_url(self):
        year, semester = member_latest_semester(self.object)
        return reverse_lazy('profiles:roster', kwargs={'year': year, 'semester': semester})


class UpdateSpecialRequirementsView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, FormView):
    """
    Processes updating special requirements from the edit person page
    Only allows POST
    """
    permission_required = 'profiles.change_person'
    group_required = 'Board Members'
    form = SpecialRequirementsForm

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
            OverrideRequirement.objects.update_or_create(year=year, semester=semester, defaults=defaults)

        redirect_year, redirect_semester = member_latest_semester(self.object)
        return redirect('profiles:roster', kwargs={'year': redirect_year, 'semester': redirect_semester})

    def form_invalid(self, form):
        try:
            person = form.data['person']
            pk = person.pk
        except:
            raise Http404
        return redirect('profiles:person-edit', kwargs={'pk': pk})


class CreateInactiveSemesterView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, View):
    """
    Processes updating inactive semesters from the edit person page
    Only allows POST
    """
    permission_required = 'profiles.create_inactivesemester'
    group_required = 'Board Members'

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

        return redirect('profiles:person-edit', kwargs={'pk': person_pk})


class DeleteInactiveSemesterView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    permission_required = 'profiles.delete_inactivesemester'
    group_required = 'Board Members'
    model = InactiveSemester

    def get_success_url(self):
        return reverse_lazy('profiles:person-edit', kwargs={'pk': self.object.person.pk})
