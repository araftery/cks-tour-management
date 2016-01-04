import datetime

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from tours.models import Tour
from shifts.models import Shift
from core.utils import now
from tours.utils import send_tour_reminder_email, send_tour_reminder_text
from shifts.utils import send_shift_reminder_email, send_shift_reminder_text


# it would be best to run these with celerybeat, but since
# we're on Heroku's free tier, the server will sleep periodically,
# so we can't rely on it being awake to send the reminders.
# instead, we'll use Heroku's scheduler with management commands.
# if running on something like EC2, however, uncomment the decorators
# below, use the .delay() method in the functions, and run celerybeat

#@periodic_task(run_every=crontab(hour=19, minute=0))
def send_reminder_emails():
    """
    Sends reminder emails for tomorrow's tours and shifts.
    """
    tomorrow = now() + datetime.timedelta(days=1)

    # get all of tomorrow's claimed tours
    tours = Tour.objects.filter(time__day=tomorrow.day, time__month=tomorrow.month, time__year=tomorrow.year).exclude(guide=None)
    for tour in tours:
        # send_tour_reminder_email.delay(tour)
        send_tour_reminder_email(tour)

    # get all of tomorrow's shifts
    shifts = Shift.objects.filter(time__day=tomorrow.day, time__month=tomorrow.month, time__year=tomorrow.year).exclude(person=None)
    for shift in shifts:
        # send_shift_reminder_email.delay(shift)
        send_shift_reminder_email(shift)


#@periodic_task(run_every=crontab(hour=8, minute=0))
def send_reminder_texts():
    """
    Sends reminder texts for today's tours and shifts.
    """
    now_obj = now()

    tours = Tour.objects.filter(time__day=now_obj.day, time__month=now_obj.month, time__year=now_obj.year, time__gte=now_obj).exclude(guide=None)
    for tour in tours:
        # send_tour_reminder_text.delay(tour)
        send_tour_reminder_text(tour)

    shifts = Shift.objects.filter(time__day=now_obj.day, time__month=now_obj.month, time__year=now_obj.year, time__gte=now_obj).exclude(person=None)
    for shift in shifts:
        # send_shift_reminder_text.delay(shift)
        send_shift_reminder_text(shift)
