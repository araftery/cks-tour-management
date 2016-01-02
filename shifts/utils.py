import calendar

from django.http import Http404

from celery.task import task

from shifts.models import Shift
from profiles.utils import get_email_by_position
from core.utils import send_email, send_text


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


@task
def send_shift_reminder_email(shift):
    source_to_positions = {
        "TEACH": ('Tour Coordinator', 'Tour Coordinator (Primary)', 'Freshman Week Coordinator'),
        "Parents' Weekend": ('Freshman Week Coordinator',),
        "Visitas": ('Freshman Week Coordinator',),
        "Comp": ('Vice President',),
        "Arts First": ('Freshman Week Coordinator',),
        "Freshman Week": ('Freshman Week Coordinator',),
        "Other": ('Freshman Week Coordinator',),
    }

    from_email = get_email_by_position(*source_to_positions.get(shift.source))
    to_person = shift.person
    to_emails = ['{} <{}>'.format(to_person.full_name, to_person.email)]
    subject = 'Shift Tomorrow at {}'.format(shift.time_local().strftime('%-I:%M %p'))

    context = {'shift': shift}
    send_email(subject, to_emails, from_email, 'email/shift_reminder.txt', 'email/shift_reminder.html', context)


@task
def send_shift_reminder_text(shift):
    to_person = shift.person

    context = {'shift': shift}
    send_text(unicode(to_person.phone), 'texts/shift_reminder.txt', context)
