from django.conf.urls import patterns, url

from shifts import views


urlpatterns = patterns('',
    url(
        regex=r'^(?P<pk>\d+)/edit/$',
        view=views.EditShiftView.as_view(),
        name='shift-edit',
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/$',
        view=views.DeleteShiftView.as_view(),
        name='shift-delete',
    ),
    url(
        regex=r'^new/$',
        view=views.CreateShiftView.as_view(),
        name='shift-new',
    ),
)
