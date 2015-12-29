from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=RedirectView.as_view(pattern_name='tours:month-noargs'),
        name='home',
    ),
)
