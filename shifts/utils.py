import calendar

from django.http import Http404

from shifts.models import Shift


def weeks_with_shifts(month=None, year=None, shifts=None, shift_kwargs=None):
    """
    Returns a list of the weeks of a given month. Each element in each week is a tuple
    in form: (date, day, shifts, canceled).

    shift_kwargs are passed to the Shift's manager's filter method
    """
    try:
        month, year = int(month), int(year)
        weeks = calendar.Calendar().monthdays2calendar(year, month)
    # if month or year is not int or are not in range
    except ValueError:
        raise Http404

    if shift_kwargs is None:
        shift_kwargs = {}

    if shifts is None:
        shifts = Shift.objects.select_related().filter(time__month=month, time__year=year, **shift_kwargs).order_by('time')

    weeks_with_shifts = []

    for week_index, week in enumerate(weeks):
        new_week = []
        for date, day in week:
            canceled = False
            new_week.append((date, day, shifts.filter(time__day=date), canceled))
        weeks_with_shifts.append(new_week)

    return weeks_with_shifts
