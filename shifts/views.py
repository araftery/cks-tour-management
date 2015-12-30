import calendar
import datetime
from dateutil.relativedelta import relativedelta

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, DeleteView, View

from braces.views import PermissionRequiredMixin

from core.utils import now, parse_year_month
from core.views import BoardOnlyMixin
from shifts.models import Shift
from shifts.forms import ShiftForm
from shifts.utils import weeks_with_shifts


class EditShiftView(PermissionRequiredMixin, BoardOnlyMixin, UpdateView):
    permission_required = 'shifts.change_shift'
    model = Shift
    form_class = ShiftForm
    template_name = 'shifts/shift_form.html'

    def get_success_url(self):
        return reverse_lazy('shifts:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class CreateShiftView(PermissionRequiredMixin, BoardOnlyMixin, CreateView):
    permission_required = 'shifts.add_shift'
    model = Shift
    form_class = ShiftForm
    template_name = 'shifts/shift_form.html'

    def get_success_url(self):
        return reverse_lazy('shifts:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class DeleteShiftView(PermissionRequiredMixin, BoardOnlyMixin, DeleteView):
    permission_required = 'shifts.delete_shift'
    model = Shift

    def get_success_url(self):
        return reverse_lazy('shifts:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class MonthView(BoardOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        now_obj = now()
        year = kwargs.get('year')
        month = kwargs.get('month')
        year, month = parse_year_month(year, month)
        months_list = [(num, name) for num, name in enumerate(list(calendar.month_name)) if num != 0]
        date = datetime.date(year, month, 1)
        next_month = date + relativedelta(months=1)
        prev_month = date + relativedelta(months=-1)

        weeks = weeks_with_shifts(month=month, year=year)

        context = {
            'months_list': months_list,
            'weeks': weeks,
            'now': now_obj,
            'month': month,
            'year': year,
            'next_year': (year + 1),
            'prev_year': (year - 1),
            'next_month': next_month,
            'prev_month': prev_month,
        }
        return render(request, 'shifts/month.html', context)
