import calendar
import datetime
import pytz

from django.conf import settings
from django.db import models

from core import utils


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

    def is_upcoming(self):
        now = utils.now()
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
        now = utils.now()

        # check if the month is open
        latest = OpenMonth.objects.filter(month=self.time.month, year=self.time.year).order_by('pk').last()

        # month is not open
        if not latest:
            return False

        # month was open, check if it's still open and the tour is in the future
        return (latest.opens <= now <= latest.closes) and self.time >= now

    def __unicode__(self):
        if self.guide is not None:
            return self.source + ', ' + self.time.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%m/%d/%y %H:%M") + ', ' + self.guide.first_name + ' ' + self.guide.last_name
        else:
            return self.source + ', ' + self.time.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%m/%d/%y %H:%M") + ', ' + 'Unclaimed'


class DefaultTour(models.Model):
    source = models.CharField(max_length=500, default="Information Office", choices=Tour.source_choices)
    minute = models.IntegerField(max_length=2)
    hour = models.IntegerField(max_length=2)
    day_num = models.IntegerField(max_length=1)
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
        return u'{} {}, opens {}, closes {}'.format(calendar.month_name[self.month], self.year, self.opens.strftime('%m/%d/%y %h:%i %a'), self.closes.strftime('%m/%d/%y %h:%i %a'))


class InitializedMonth(models.Model):
    month = models.IntegerField(max_length=2)
    year = models.IntegerField(max_length=4)

    def __unicode__(self):
        return u'{} {}'.format(calendar.month_name[self.month], self.year)


class CanceledDay(models.Model):
    date = models.DateField()
