import calendar
import datetime
import pytz

from django.conf import settings
from django.db import models

from core import utils as core_utils


class TaskQuerySet(models.QuerySet):
    """
    QuerySet for tours and shifts.
    """
    def semester(self, semester=None, year=None):
        """
        Includes only members who are inactive for the given semester and year
        """
        year, semester = core_utils.parse_year_semester(year=year, semester=semester)
        start, end = core_utils.semester_bounds(semester=semester, year=year)

        return self.filter(time__gte=start, time__lte=end)


class Tour(models.Model):
    source_choices_flat = [
        "Information Office",
        "Marshall's Office",
        "Alumni Association",
        "Admissions Office",
        "Visitas",
        "Parents' Weekend",
        "Comp",
        "Other",
    ]

    source_choices = [(i, i) for i in source_choices_flat]

    source = models.CharField(max_length=500, default="Information Office")
    guide = models.ForeignKey('profiles.Person', null=True, blank=True, related_name='tours')
    time = models.DateTimeField()
    notes = models.TextField(max_length=2000, blank=True)
    missed = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    length = models.IntegerField(max_length=3, default=75, null=True)
    counts_for_requirements = models.BooleanField(default=True)

    # true if tour was made during the initialization process
    default_tour = models.BooleanField(default=False)

    # custom manager
    objects = TaskQuerySet.as_manager()

    def time_local(self):
        return core_utils.localize_time(self.time)

    def is_upcoming(self):
        now = core_utils.now()
        if self.time > now:
            return True
        else:
            return False

    def is_unclaimed(self):
        if self.guide is None:
            return True
        else:
            return False

    @property
    def claim_eligible(self):
        from tours.utils import month_is_open
        now = core_utils.now()

        # check if the month is open
        if not month_is_open(month=self.time.month, year=self.time.year):
            return False

        # month is open, check if the tour is in the future
        return self.time >= now

    def __unicode__(self):
        if self.guide is not None:
            return self.source + ', ' + self.time.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%m/%d/%y %H:%M") + ', ' + self.guide.first_name + ' ' + self.guide.last_name
        else:
            return self.source + ', ' + self.time.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%m/%d/%y %H:%M") + ', ' + 'Unclaimed'


class DefaultTour(models.Model):
    source = models.CharField(max_length=500, default="Information Office", choices=Tour.source_choices)
    minute = models.IntegerField(max_length=2)
    hour = models.IntegerField(max_length=2)
    day_num = models.IntegerField(max_length=1, choices=list(enumerate(calendar.day_name)))
    notes = models.TextField(max_length=2000, blank=True)
    length = models.IntegerField(max_length=3, default=75)

    @property
    def time(self):
        return datetime.datetime(2000, 1, 1, self.hour, self.minute)

    def __unicode__(self):
        return self.source + ', ' + unicode(calendar.day_name[self.day_num]) + 's ' + datetime.datetime(2000, 1, 1, self.hour, self.minute).strftime("%H:%M")


class OpenMonth(models.Model):
    month = models.IntegerField(max_length=2)
    year = models.IntegerField(max_length=4)
    opens = models.DateTimeField()
    closes = models.DateTimeField()

    def __unicode__(self):
        return u'{} {}, opens {}, closes {}'.format(calendar.month_name[self.month], self.year, self.opens.strftime('%m/%d/%y %h:%M %a'), self.closes.strftime('%m/%d/%y %h:%M %a'))


class InitializedMonth(models.Model):
    month = models.IntegerField(max_length=2)
    year = models.IntegerField(max_length=4)

    def __unicode__(self):
        return u'{} {}'.format(calendar.month_name[self.month], self.year)


class CanceledDay(models.Model):
    date = models.DateField()
