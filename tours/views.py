import calendar
from collections import Counter
import datetime
from dateutil.relativedelta import relativedelta

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, CreateView, DeleteView

from braces.views import (
    PermissionRequiredMixin,
    MultiplePermissionsRequiredMixin,
)

from core.views import BoardOnlyMixin
from core import utils
from tours.models import Tour, CanceledDay, DefaultTour, InitializedMonth, OpenMonth
from tours.forms import TourForm, ChooseMonthForm, OpenMonthForm
from tours import utils as tours_utils


class MonthView(BoardOnlyMixin, View):

    def get(self, request, *args, **kwargs):
        now = utils.now()
        year = kwargs.get('year')
        month = kwargs.get('month')
        year, month = utils.parse_year_month(year, month)
        months_list = [(num, name) for num, name in enumerate(list(calendar.month_name)) if num != 0]
        date = datetime.date(year, month, 1)
        next_month = date + relativedelta(months=1)
        prev_month = date + relativedelta(months=-1)

        is_open, date_closes = tours_utils.month_is_open(month=month, year=year, return_tuple=True)

        if is_open:
            public_url = None
            # TODO
            #public_url = request.build_absolute_uri(reverse_lazy('public:month', kwargs={'year': year, 'month': month}))
        else:
            public_url = None

        open_eligible = tours_utils.open_eligible(month=month, year=year)

        weeks_with_tours = tours_utils.weeks_with_tours(month=month, year=year)

        context = {
            'months_list': months_list,
            'weeks': weeks_with_tours,
            'now': now,
            'month': month,
            'year': year,
            'next_year': (year + 1),
            'prev_year': (year - 1),
            'next_month': next_month,
            'prev_month': prev_month,
            'month_initialized': tours_utils.is_initialized(month=month, year=year),
            'is_open': is_open,
            'date_closes': date_closes,
            'open_eligible': open_eligible,
            'public_url': public_url
        }

        if kwargs.get('print') is True:
            return render(request, 'tours/month_print.html', context)
        else:
            return render(request, 'tours/month.html', context)


class EditTourView(PermissionRequiredMixin, BoardOnlyMixin, UpdateView):
    permission_required = 'tours.change_tour'
    model = Tour
    form_class = TourForm
    template_name = 'tours/tour_form.html'

    def get_success_url(self):
        return reverse_lazy('tours:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class CreateTourView(PermissionRequiredMixin, BoardOnlyMixin, CreateView):
    permission_required = 'tours.add_tour'
    model = Tour
    form_class = TourForm
    template_name = 'tours/tour_form.html'

    def get_success_url(self):
        return reverse_lazy('tours:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class DeleteTourView(PermissionRequiredMixin, BoardOnlyMixin, DeleteView):
    permission_required = 'tours.delete_tour'
    model = Tour

    def get_success_url(self):
        return reverse_lazy('tours:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class InitializeMonthView(MultiplePermissionsRequiredMixin, BoardOnlyMixin, View):
    permissions = {
        "all": ('tours.add_tour', 'tours.add_canceledday', 'tours.add_initializedmonth',),
        "any": (),
    }

    def get(self, request, *args, **kwargs):
        month = kwargs.get('month')
        year = kwargs.get('year')
        year, month = utils.parse_year_month(year, month, default=None)
        now = utils.now()

        if not month or not year:
            # show choose form
            choose_month_form = ChooseMonthForm()
            return render(request, 'tours/initialize_choose_month.html', {'form': choose_month_form})

        try:
            month = int(month)
            year = int(year)
        except:
            raise Http404

        # make sure this month isn't initialized or out of allowed range
        date_obj = datetime.datetime(year, month, 1)
        current = datetime.datetime(now.year, now.month, 1)
        last_allowed = utils.add_months(current, 12, True)

        # make sure this month isn't initialized or out of allowed range
        if tours_utils.is_initialized(month=month, year=year) or date_obj < current or date_obj > last_allowed:
            raise PermissionDenied

        weeks = calendar.Calendar().monthdays2calendar(year, month)
        return render(request, 'tours/initialize_month.html', {'weeks': weeks, 'month': month, 'year': year})

    def post(self, request, *args, **kwargs):
        month = kwargs.get('month')
        year = kwargs.get('year')
        year, month = utils.parse_year_month(year, month)
        now = utils.now()

        try:
            month = int(month)
            year = int(year)
        except:
            raise Http404

        # make sure this month isn't initialized or out of allowed range
        date_obj = datetime.datetime(year, month, 1)
        current = datetime.datetime(now.year, now.month, 1)
        last_allowed = utils.add_months(current, 12, True)

        # make sure this month isn't initialized or out of allowed range
        if tours_utils.is_initialized(month=month, year=year) or date_obj < current or date_obj > last_allowed:
            raise PermissionDenied

        # process form
        selected_days = request.POST.get('selected_days', None)
        if selected_days is None:
            return HttpResponseBadRequest

        # make a counter of all selected days (i.e., days on which to have tours)
        if selected_days != '':
            selected_days_counter = Counter([int(i) for i in selected_days.split(',')])
        else:
            selected_days_counter = Counter()

        # make a counter of all days in the month
        month_dates_counter = Counter([i for i in calendar.Calendar().itermonthdays(year, month) if i != 0])
        canceled_days_counter = month_dates_counter - selected_days_counter

        for num, times in canceled_days_counter.items():
            date = datetime.date(year, month, num)
            canceled_day = CanceledDay(date=date)
            canceled_day.save()

        # add default tours on non-blacked out days
        default_tours = DefaultTour.objects.all()
        weeks = calendar.Calendar().monthdatescalendar(year, month)
        for week in weeks:
            for date in week:
                if date.month == month and not CanceledDay.objects.filter(date=date):
                    for default_tour in default_tours.filter(day_num=date.weekday):
                        add_tour = Tour.objects.create(
                            source=default_tour.source,
                            time=datetime.datetime(date.year, date.month, date.day, default_tour.hour, default_tour.minute),
                            notes=default_tour.notes,
                            length=default_tour.length,
                            default_tour=True
                        )

        # mark month as initialized
        initialized_month = InitializedMonth.objects.create(month=month, year=year)
        return redirect('tours:month', month=month, year=year)


class UninitializeMonthView(MultiplePermissionsRequiredMixin, BoardOnlyMixin, View):
    permissions = {
        "all": ('tours.delete_canceledday', 'tours.delete_initializedmonth', 'tours.delete_tour',),
        "any": (),
    }

    def get(self, request, *args, **kwargs):
        try:
            month = kwargs.get('month')
            year = kwargs.get('year')
            year, month = utils.parse_year_month(year, month, default=None)
            obj = InitializedMonth.objects.get(month=month, year=year)
        except InitializedMonth.DoesNotExist:
            raise Http404
        return render(request, 'tours/uninitialize_confirm.html', {'month': month, 'year': year})

    def post(self, request, *args, **kwargs):
        try:
            month = kwargs.get('month')
            year = kwargs.get('year')
            obj = InitializedMonth.objects.get(month=month, year=year)
        except InitializedMonth.DoesNotExist:
            raise Http404

        # delete default tours
        Tour.objects.filter(time__month=month, time__year=year, default_tour=True).delete()

        # delete canceled days
        CanceledDay.objects.filter(date__month=month, date__year=year).delete()

        # delete initialization object
        obj.delete()

        # close month if open
        OpenMonth.objects.filter(month=month, year=year).delete()

        return redirect('tours:month', month=month, year=year)


class CreateOpenMonthView(PermissionRequiredMixin, BoardOnlyMixin, CreateView):
    permission_required = 'tours.add_openmonth'
    model = OpenMonth
    form_class = OpenMonthForm
    template_name = 'tours/open_month_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateOpenMonthView, self).get_context_data(**kwargs)
        context['year'] = self.kwargs.get('year')
        context['month'] = self.kwargs.get('month')

        return context

    def get_success_url(self):
        return reverse_lazy('tours:month', kwargs={'year': self.object.year, 'month': self.object.month})

    def get_initial(self):
        now = utils.now()
        closes_default = (now + datetime.timedelta(days=7)).replace(hour=17, minute=0, second=0, microsecond=0)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        year, month = utils.parse_year_month(year, month, default=None)
        return {'opens': now, 'closes': closes_default, 'month': month, 'year': year}


class EditOpenMonthView(PermissionRequiredMixin, BoardOnlyMixin, UpdateView):
    permission_required = 'tours.update_openmonth'
    model = OpenMonth
    form_class = OpenMonthForm
    template_name = 'tours/open_month_form.html'

    def get_object(self, queryset):
        latest = OpenMonth.objects.filter(month=self.month, year=self.year).order_by('closing').last()

        if not latest:
            raise Http404

        return latest

    def get_context_data(self, **kwargs):
        context = super(EditOpenMonthView, self).get_context_data(**kwargs)
        context['year'] = self.kwargs.get('year')
        context['month'] = self.kwargs.get('month')

        return context

    def get_success_url(self):
        return reverse_lazy('tours:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class CloseMonthView(PermissionRequiredMixin, BoardOnlyMixin, View):
    permission_required = 'tours.delete_openmonth'

    def post(self, request, *args, **kwargs):
        month = kwargs.get('month')
        year = kwargs.get('year')
        year, month = utils.parse_year_month(year, month, default=None)

        OpenMonth.objects.filter(month=month, year=year).delete()

        return redirect('tours:month', year=year, month=month)
