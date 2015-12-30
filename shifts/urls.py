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
    url(
        regex=r'^month/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view=views.MonthView.as_view(),
        name='month',
    ),
    url(
        regex=r'^month/$',
        view=views.MonthView.as_view(),
        name='month-noargs',
    ),
)
