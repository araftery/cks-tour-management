from django.contrib.auth import logout
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from braces.views import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    GroupRequiredMixin,
)

from core.models import Setting
from core.setting_validators import setting_validators


class BoardOnlyMixin(LoginRequiredMixin, GroupRequiredMixin):
    group_required = 'Board Members'


class SettingsView(PermissionRequiredMixin, BoardOnlyMixin, View):
    permission_required = 'core.change_setting'

    def get(self, request, *args, **kwargs):
        settings = Setting.objects.all().order_by('order_num')
        settings_vals = []
        for setting in settings:
            # setting, value, [errors]
            settings_vals.append((setting, setting.value, None))
        return render(request, 'core/settings.html', {'settings': settings_vals})

    def post(self, request, *args, **kwargs):
        settings = Setting.objects.all().order_by('order_num')
        form_data = []
        form_validation = []

        for setting in settings:
            form_data.append(setting, request.POST.get('setting_{}'.format(setting.name)))

        for setting, data in settings:
            validation = setting_validators[setting.value_type](setting.value)
            form_validation.append((setting, validation))

        if all([x[1]['valid'] for x in form_validation]):
            # form is valid, save and redirect
            for setting, validation in form_validation:
                new_value = validation['value']
                setting.value = new_value
                setting.save()
            return redirect('core:settings')
        else:
            # form is invalid, show errors
            settings_vals = []
            for setting, validation in form_validation:
                settings_vals.append((setting, validation['value'], validation['errors']))

            return render(request, 'core/settings.html', {'settings': settings_vals})


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
