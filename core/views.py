from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import logout
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from braces.views import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    GroupRequiredMixin,
)

from core.forms import SettingFormSet
from core.models import Setting
from profiles.models import Person
from profiles.utils import get_email_by_position
from tours.models import DefaultTour


class BoardOnlyMixin(LoginRequiredMixin, GroupRequiredMixin):
    group_required = 'Board Members'


class SettingsView(BoardOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        existing_settings = Setting.objects.raw('SELECT DISTINCT core_setting.id, core_setting.order_num FROM core_setting INNER JOIN (SELECT MAX(id) AS id FROM core_setting GROUP BY name) maxid ON core_setting.id = maxid.id ORDER BY core_setting.order_num ASC')
        settings = Setting.objects.filter(id__in=(x.pk for x in existing_settings)).order_by('order_num')
        formset = SettingFormSet(queryset=settings)
        default_tours = DefaultTour.objects.all().order_by('day_num', 'hour', 'minute')
        return render(request, 'core/settings.html', {'formset': formset, 'default_tours': default_tours})

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('core.change_setting'):
            raise PermissionDenied
        data = request.POST
        formset = SettingFormSet(data)
        if formset.is_valid():
            formset.save()
            return redirect('core:settings')
        else:
            default_tours = DefaultTour.objects.all().order_by('day_num', 'hour', 'minute')
            return render(request, 'core/settings.html', {'formset': formset, 'default_tours': default_tours})


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.person.is_board:
            return redirect('tours:month-noargs')
        else:
            return redirect('public:home')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("core:home")

        return render(request, 'social_auth/login.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('core:home')


@csrf_exempt
def text_response(request):
    from_email = to_email = get_email_by_position('Secretary', 'Tour Coordinator (Primary)', 'Tour Coordinator')

    text = request.POST.get('Body')
    from_number = request.POST.get('From')

    if text is None or from_number is None:
        raise PermissionDenied

    try:
        person = Person.objects.get(phone=from_number)
        from_ = person.full_name
    except Person.DoesNotExist:
        from_ = from_number

    msg = EmailMultiAlternatives(u'Text Message to CKS Twilio Account', 'Message from {}: {}'.format(from_, text), from_email, [to_email])
    msg.send()

    return render(request, 'core/response.xml', content_type="text/xml")
