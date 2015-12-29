from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView

from braces.views import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    GroupRequiredMixin,
)

from shifts.models import Shift
from shifts.forms import ShiftForm


class EditShiftView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    permission_required = 'shifts.change_tour'
    group_required = 'Board Members'
    model = Shift
    form_class = ShiftForm
    template_name = 'shifts/shift_form.html'

    def get_success_url(self):
        return reverse_lazy('shifts:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class CreateShiftView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    permission_required = 'shifts.add_shift'
    group_required = 'Board Members'
    model = Shift
    form_class = ShiftForm
    template_name = 'shifts/shift_form.html'

    def get_success_url(self):
        return reverse_lazy('shifts:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})


class DeleteShiftView(PermissionRequiredMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    permission_required = 'shifts.delete_shift'
    group_required = 'Board Members'
    model = Shift

    def get_success_url(self):
        return reverse_lazy('shifts:month', kwargs={'year': self.object.time.year, 'month': self.object.time.month})
