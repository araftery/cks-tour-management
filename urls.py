from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^', include('core.urls', namespace='core', app_name='core')),
    url(r'^tours/', include('tours.urls', namespace='tours', app_name='tours')),
    url(r'^shifts/', include('shifts.urls', namespace='shifts', app_name='shifts')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles', app_name='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)
