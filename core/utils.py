import calendar
import datetime
import pytz

from django.conf import settings
from django.http import Http404
from django.utils import timezone

from core.models import Setting


def now():
    return timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))


def current_semester(now_obj=None):
    """
    Given a datetime.datetime object, figures out the current semester based on
    the start and end points defined in settings. Returns either 'fall' or 'spring,'
    or None if something goes wrong
    """
    if now_obj is None:
        now_obj = now()

    now_date = now_obj.date()

    fall_start = datetime.date(now_obj.year, *settings.FALL_SEMESTER_START)
    fall_end = datetime.date(now_obj.year, *settings.FALL_SEMESTER_END)

    spring_start = datetime.date(now_obj.year, *settings.SPRING_SEMESTER_START)
    spring_end = datetime.date(now_obj.year, *settings.SPRING_SEMESTER_END)

    if fall_start <= now_date <= fall_end:
        return 'fall'
    elif spring_start <= now_date <= spring_end:
        return 'spring'
    else:
        return None


def parse_year_month(year, month, default='now'):
    if default == 'now':
        default = now()
    elif callable(default):
        default = default()

    if year is None and month is None:
        if default:
            year = default.year
            month = default.month
    elif not year or not month:
        raise Http404
    else:
        try:
            year = int(year)
            month = int(month)
        except:
            raise Http404

    return year, month


def add_months(sourcedate, months, return_datetime=False):
    """
    Takes a source datetime.datetime or datetime.date and adds a number of months.
    Returns a datetime.date by default, but can also returrn a datetime.datetime object.
    """
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    if not return_datetime:
        return datetime.date(year, month, day)
    else:
        return datetime.datetime(year, month, day)


def class_years(semester=None, year=None, bookends_only=False):
    """
    Given a semester and year, returns a tuple of the class years currently in school, in ascending order.
    >>> class_years('fall', 2013)
    >>> (2014, 2015, 2016, 2017)
    """
    if semester is None:
        semester = current_semester()
    if year is None:
        year = now().year
    else:
        year = int(year)
        semester = semester.lower()

    if semester == 'fall':
        years = range(year + 1, year + 5)
    elif semester == 'spring':
        years = range(year, year + 4)
    else:
        raise ValueError('Semester must either fall or spring.')

    if bookends_only is True:
        return (years[0], years[3])
    else:
        return years


def get_default_num_tours():
    num = Setting.objects.filter(name=settings.DEFAULT_NUM_TOURS_SETTING_NAME).last().value
    return int(num)


def get_default_num_shifts():
    num = Setting.objects.filter(name=settings.DEFAULT_NUM_SHIFTS_SETTING_NAME).last().value
    return int(num)
