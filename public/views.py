from django.core.exceptions import PermissionDenied
from django.views.generic import View, RedirectView
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from braces.views import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from tours.models import Tour
from core.utils import parse_year_semester, delta_semester, dues_required
from profiles.utils import get_person_by_position


class MemberIsActiveMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self, user):
        return user.person.is_active()


class HomeView(MemberIsActiveMixin, RedirectView):
    pattern_name = 'public:month-noargs'


class TourClaimView(MemberIsActiveMixin, View):
    def get_obj(self, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(Tour, pk=pk)

        if obj.guide is not None or not obj.claim_eligible:
            raise PermissionDenied

        return obj

    def get(self, request, *args, **kwargs):
        tour = self.get_obj(*args, **kwargs)
        return render(request, 'public/claim_confirm.html', {'tour': tour})

    def post(self, request, *args, **kwargs):
        tour = self.get_obj(*args, **kwargs)
        tour.guide = request.user.person
        tour.save()
        return redirect('public:month', month=tour.time_local().month, year=tour.time_local().year)


class TourUnclaimView(MemberIsActiveMixin, View):
    def get_obj(self, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(Tour, pk=pk)

        if obj.guide != self.request.user.person or not obj.claim_eligible:
            raise PermissionDenied

        return obj

    def get(self, request, *args, **kwargs):
        tour = self.get_obj(*args, **kwargs)
        return render(request, 'public/unclaim_confirm.html', {'tour': tour})

    def post(self, request, *args, **kwargs):
        tour = self.get_obj(*args, **kwargs)
        tour.guide = None
        tour.save()
        return redirect('public:month', month=tour.time_local().month, year=tour.time_local().year)


class ProfileView(MemberIsActiveMixin, View):
    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        semester = kwargs.get('semester')
        year, semester = parse_year_semester(year, semester)
        prev_semester = delta_semester(semester=semester, year=year, delta=-1, as_dict=True)
        next_semester = delta_semester(semester=semester, year=year, delta=1, as_dict=True)
        collect_dues = dues_required(semester=semester, year=year)
        person = request.user.person

        if not person.is_active(semester=next_semester['semester'], year=next_semester['year']):
            next_semester = None

        if not person.is_active(semester=prev_semester['semester'], year=prev_semester['year']):
            prev_semester = None

        person.cached_status = {
            'tours_status': person.tours_status(year=year, semester=semester),
            'shifts_status': person.shifts_status(year=year, semester=semester),
            'dues_status': person.dues_status(year=year, semester=semester),
        }

        # determine status
        tours_status = person.cached_status['tours_status']['status']
        shifts_status = person.cached_status['shifts_status']['status']
        dues_status = person.cached_status['dues_status']

        statuses = (tours_status, shifts_status, dues_status)

        if tours_status == 'incomplete' or shifts_status == 'incomplete' or dues_status == 'incomplete':
            status = 'incomplete'
        elif all([x in ('complete', 'projected', 'not_required') for x in statuses]) and any([x == 'projected' for x in statuses]):
            status = 'projected'
        else:
            status = 'complete'

        status_names = {
            'incomplete': 'Requirements Incomplete',
            'projected': 'Projected to Complete',
            'complete': 'Requirements Complete',
        }

        context = {
            'person': person,
            'status_class': status,
            'status': status_names[status],
            'tours': person.tours.semester(year=year, semester=semester).order_by('time'),
            'shifts': person.shifts.semester(year=year, semester=semester).order_by('time'),
            'next_semester': next_semester,
            'prev_semester': prev_semester,
            'collect_dues': collect_dues,
        }

        return render(request, 'public/profile.html', context)


class HelpView(MemberIsActiveMixin, View):
    def get(self, request, *args, **kwargs):
        secretary = get_person_by_position('Secretary')
        tour_coordinator = get_person_by_position('Tour Coordinator (Primary)', 'Tour Coordinator')
        markdown = render_to_string('public/documentation.md', {'tour_coordinator': tour_coordinator, 'secretary': secretary})
        return render(request, 'public/help.html', {'markdown': markdown})
