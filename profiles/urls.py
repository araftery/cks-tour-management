from django.conf.urls import patterns, url

from profiles import views


urlpatterns = patterns('',
    url(
        regex=r'^person/(?P<pk>\d+)/edit/$',
        view=views.EditPersonView.as_view(),
        name='person-edit',
    ),
    url(
        regex=r'^person/(?P<pk>\d+)/delete/$',
        view=views.DeletePersonView.as_view(),
        name='person-delete',
    ),
    url(
        regex=r'^person/new/$',
        view=views.CreatePersonView.as_view(),
        name='person-new',
    ),
    url(
        regex=r'^person/bulk-new/$',
        view=views.BulkCreatePersonView.as_view(),
        name='person-new-bulk',
    ),
    url(
        regex=r'^special-requirements/$',
        view=views.UpdateSpecialRequirementsView.as_view(),
        name='special-requirements-update',
    ),
    url(
        regex=r'^person/(?P<pk>\d+)/inactive-semester/new/$',
        view=views.CreateInactiveSemesterView.as_view(),
        name='inactive-semester-new',
    ),
    url(
        regex=r'^inactive-semester/(?P<pk>\d+)/delete/$',
        view=views.DeleteInactiveSemesterView.as_view(),
        name='inactive-semester-delete',
    ),
    url(
        regex=r'^roster/$',
        view=views.RosterView.as_view(),
        name='roster-noargs',
    ),
    url(
        regex=r'^roster/(?P<year>\d{4})/(?P<semester>\w+)/$',
        view=views.RosterView.as_view(),
        name='roster',
    ),
    url(
        regex=r'^roster/vcard/$',
        view=views.RosterVCardView.as_view(),
        name='roster-vcard-noargs',
    ),
    url(
        regex=r'^roster/(?P<year>\d{4})/(?P<semester>\w+)/vcard/$',
        view=views.RosterVCardView.as_view(),
        name='roster-vcard',
    ),
)
