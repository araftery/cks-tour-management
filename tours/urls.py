from django.conf.urls import patterns, url

from tours import views


urlpatterns = patterns('',
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
    url(
        regex=r'^month/(?P<year>\d{4})/(?P<month>\d{1,2})/edit/$',
        view=views.MonthEditView.as_view(),
        name='month-edit',
    ),
    url(
        regex=r'^(?P<pk>\d+)/edit/$',
        view=views.EditTourView.as_view(),
        name='tour-edit',
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/$',
        view=views.DeleteTourView.as_view(),
        name='tour-delete',
    ),
    url(
        regex=r'^new/$',
        view=views.CreateTourView.as_view(),
        name='tour-new',
    ),
    url(
        regex=r'^month/(?P<year>\d{4})/(?P<month>\d{1,2})/initialize/$',
        view=views.InitializeMonthView.as_view(),
        name='month-initialize',
    ),
    url(
        regex=r'^month/initialize/$',
        view=views.InitializeMonthView.as_view(),
        name='month-initialize-noargs',
    ),
)
