import pytz

from django.db import models

from core import utils


class Shift(models.Model):
    source_choices_flat = (
        "TEACH",
        "Parents' Weekend",
        "Visitas",
        "Comp",
        "Arts First",
        "Freshman Week",
        "Other",
    )

    source_choices = [(i, i) for i in source_choices_flat]

    source = models.CharField(max_length=500)
    person = models.ForeignKey('profiles.Person', related_name='shifts', null=True, blank=True)
    time = models.DateTimeField()
    notes = models.TextField(max_length=2000, blank=True)
    missed = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    length = models.IntegerField(max_length=3, blank=True, null=True)
    counts_for_requirements = models.BooleanField(default=True)

    def is_missed(self):
        if self.missed:
            return True
        else:
            return False

    def is_late(self):
        if self.late:
            return True
        else:
            return False

    def is_unclaimed(self):
        if self.person is None:
            return True
        else:
            return False

    @property
    def is_upcoming(self):
        now = utils.now()
        if self.time > now:
            return True
        else:
            return False

    def __unicode__(self):
        if self.person is not None:
            return self.source + ', ' + self.time.astimezone(pytz.timezone('America/New_York')).strftime("%m/%d/%y %H:%M") + ', ' + self.person.first_name + ' ' + self.person.last_name
        else:
            return self.source + ', ' + self.time.astimezone(pytz.timezone('America/New_York')).strftime("%m/%d/%y %H:%M") + ', ' + 'Unclaimed'
