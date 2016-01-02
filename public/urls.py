from django.conf.urls import patterns, url

from public import views
from tours.views import MonthView


urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=views.HomeView.as_view(),
        name='home',
    ),
    url(
        regex=r'^profile/$',
        view=views.ProfileView.as_view(),
        name='profile-noargs',
    ),
    url(
        regex=r'^profile/(?P<year>\d{4})/(?P<semester>\w+)/$',
        view=views.ProfileView.as_view(),
        name='profile',
    ),
    url(
        regex=r'^month/$',
        view=MonthView.as_view(),
        name='month-noargs',
        kwargs={'public': True}
    ),
    url(
        regex=r'^month/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view=MonthView.as_view(),
        name='month',
        kwargs={'public': True}
    ),
    url(
        regex=r'^tours/(?P<pk>\d+)/claim/$',
        view=views.TourClaimView.as_view(),
        name='tour-claim',
    ),
    url(
        regex=r'^tours/(?P<pk>\d+)/unclaim/$',
        view=views.TourUnclaimView.as_view(),
        name='tour-unclaim',
    ),
    url(
        regex=r'^help/$',
        view=views.HelpView.as_view(),
        name='help',
    ),
)
