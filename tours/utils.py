import calendar
import datetime

from django.http import Http404

from core import utils
from tours.models import Tour, OpenMonth, CanceledDay, InitializedMonth


def month_is_open(month, year, return_tuple=False):
    """
    Checks if a month is 'open' for tour claiming.
    Returns True/False. Optionally returns a tuple that also includes the closing date.
    """
    now = utils.now()

    try:
        latest = OpenMonth.objects.filter(month=month, year=year).latest('pk')
    except OpenMonth.DoesNotExist:
        latest = None

    if latest:
        if latest.opens <= now <= latest.closes:
            if return_tuple:
                return True, latest.closes
            else:
                return True
        else:
            if return_tuple:
                return False, None
            else:
                return False
    else:
        if return_tuple:
            return False, None
        else:
            return False


def is_initialized(month, year):
    initialized_month = InitializedMonth.objects.filter(month=month, year=year)
    if initialized_month:
        return True
    else:
        return False


def open_eligible(month, year):
    """
    Checks whether a month is eligible to be opened. That is, it has not passed yet and is in the current semester.
    """
    now = utils.now()
    month = int(month)
    year = int(year)

    # whether the month is in the current semester
    in_current_semester = (utils.current_semester(now) == utils.current_semester(datetime.datetime(year, month, 1))) and year == now.year

    # month is in the current semester, and is the current month or in the future, and the month is initialized
    if in_current_semester and month >= now.month and is_initialized(month=month, year=year):
        return True
    else:
        return False


def weeks_with_tours(month=None, year=None, tours=None, tour_kwargs=None):
    """
    Returns a list of the weeks of a given month. Each element in each week is a tuple
    in form: (date, day, tours, canceled).

    tour_kwargs are passed to the Tour's manager's filter method
    """
    try:
        month, year = int(month), int(year)
        weeks = calendar.Calendar().monthdays2calendar(year, month)
    # if month or year is not int or are not in range
    except ValueError:
        raise Http404

    if tour_kwargs is None:
        tour_kwargs = {}

    if tours is None:
        tours = Tour.objects.select_related().filter(time__month=month, time__year=year, **tour_kwargs).order_by('time')

    canceled_days = CanceledDay.objects.filter(date__month=month, date__year=year).order_by('date')
    canceled_days_dict = {}
    for day in canceled_days:
        canceled_days_dict[day.date.day] = True

    weeks_with_tours = []

    for week_index, week in enumerate(weeks):
        new_week = []
        for date, day in week:
            if date != 0:
                canceled = canceled_days_dict.get(date, False)
            else:
                canceled = False
            new_week.append((date, day, tours.filter(time__day=date), canceled))
        weeks_with_tours.append(new_week)

    return weeks_with_tours


def get_initialize_month_choices():
    now = utils.now()
    months = [utils.add_months(now, i) for i in range(0, 13)]
    months_choices = []
    for month in months:
        if not is_initialized(month=month.month, year=month.year):
            months_choices.append((u'{}/{}'.format(month.year, month.month), month.strftime('%B %Y')))
    return months_choices
