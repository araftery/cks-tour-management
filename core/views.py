from django.contrib.auth import logout
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from braces.views import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    GroupRequiredMixin,
)

from core.forms import SettingFormSet
from core.models import Setting
from tours.models import DefaultTour


class BoardOnlyMixin(LoginRequiredMixin, GroupRequiredMixin):
    group_required = 'Board Members'


class SettingsView(PermissionRequiredMixin, BoardOnlyMixin, View):
    permission_required = 'core.change_setting'

    def get(self, request, *args, **kwargs):
        existing_settings = Setting.objects.raw('SELECT DISTINCT core_setting.id, core_setting.order_num FROM core_setting INNER JOIN (SELECT MAX(id) AS id FROM core_setting GROUP BY name) maxid ON core_setting.id = maxid.id ORDER BY core_setting.order_num ASC')
        settings = Setting.objects.filter(id__in=(x.pk for x in existing_settings)).order_by('order_num')
        formset = SettingFormSet(queryset=settings)
        default_tours = DefaultTour.objects.all().order_by('day_num', 'hour', 'minute')
        return render(request, 'core/settings.html', {'formset': formset, 'default_tours': default_tours})

    def post(self, request, *args, **kwargs):
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
            # TODO: redirect to public site
            # return redirect('public:home')
            raise PermissionDenied


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("core:home")

        return render(request, 'social_auth/login.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('core:home')
