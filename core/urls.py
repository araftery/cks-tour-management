from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from core import views


urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=views.HomeView.as_view(),
        name='home',
    ),
    url(
        regex=r'^settings/$',
        view=views.SettingsView.as_view(),
        name='settings',
    ),
    url(
        regex=r'^login/$',
        view=views.LoginView.as_view(),
        name='login',
    ),
    url(
        regex=r'^logout/$',
        view=views.LogoutView.as_view(),
        name='logout',
    ),
    url(
        regex=r'^text-response/$',
        view=views.text_response,
        name='text-response',
    ),
)
