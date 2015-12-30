import vobject

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from core import utils


class PersonQuerySet(models.QuerySet):
    def inactive(self, semester=None, year=None):
        """
        Includes only members who are inactive for the given semester and year
        """
        if semester is None:
            semester = utils.current_semester()
        if year is None:
            year = utils.now().year
        else:
            year = int(year)
            semester = semester.lower()

        return self.filter(inactive_semesters__year__exact=year, inactive_semesters__semester=semester)

    def active(self, semester=None, year=None):
        """
        Excludes members who are inactive for the given semester and year
        """
        if semester is None:
            semester = utils.current_semester()
        if year is None:
            year = utils.now().year
        else:
            year = int(year)

        semester = semester.lower()

        return self.exclude(inactive_semesters__year__exact=year, inactive_semesters__semester=semester)

    def current_members(self, semester=None, year=None):
        if semester is None:
            semester = utils.current_semester()
        if year is None:
            year = utils.now().year
        else:
            year = int(year)
            semester = semester.lower()

        senior_year, freshman_year = utils.class_years(semester=semester, year=year, bookends_only=True)

        kwargs = {}

        if semester == 'fall':
            kwargs['member_since_year__lte'] = year
        else:
            kwargs['member_since_year__lt'] = year

        kwargs['year__lte'] = freshman_year
        kwargs['year__gte'] = senior_year

        return self.filter(**kwargs)


class Person(models.Model):
    user = models.OneToOneField('auth.User', null=True, blank=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    harvard_email = models.EmailField()
    phone = PhoneNumberField()
    year = models.IntegerField(max_length=4)
    notes = models.TextField(max_length=2000, blank=True)

    titles = ['President', 'Vice President', 'Treasurer', 'Secretary', 'Tour Coordinator (Primary)', 'Tour Coordinator', 'Freshman Week Coordinator', 'Other Board Member', 'Regular Member']

    positions_choices = [(i, i) for i in titles]
    position = models.CharField(max_length=50, choices=positions_choices, default='Regular Member')
    site_admin = models.BooleanField(default=False)

    # member since fall of...
    member_since_year = models.IntegerField(max_length=4)

    houses = ('Adams', 'Quincy', 'Lowell', 'Eliot', 'Kirkland', 'Winthrop', 'Mather', 'Leverett', 'Dunster', 'Cabot', 'Pforzheimer', 'Currier', 'Dudley', 'Freshman (Yard)')
    houses_choices = [(house, house) for house in houses]
    house = models.CharField(choices=houses_choices, max_length=50, blank=True, null=True)

    # custom manager
    objects = PersonQuerySet.as_manager()

    def phone_display(self):
        """
        Removes the +1 from the phone number if it exists.
        """
        phone = unicode(self.phone)
        if phone[:2] == '+1':
            return phone[2:]
        else:
            return phone

    @property
    def is_active(self):
        if self._default_manager.active().current_members().filter(pk=self.pk):
            return True
        else:
            return False

    @property
    def is_board(self):
        return self.user.groups.filter(name='Board Members').count() != 0

    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def as_vcard(self):
        v = vobject.vCard()
        v.add('n')
        v.n.value = vobject.vcard.Name(family=self.last_name, given=self.first_name)
        v.add('fn')
        v.fn.value = self.full_name
        v.add('email')
        v.email.value = self.email
        v.add('tel')
        v.tel.value = self.phone
        v.tel.type_param = 'MOBILE'
        output = v.serialize()
        return output

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)


class InactiveSemester(models.Model):
    year = models.IntegerField(max_length=4)
    semesters_choices = [('fall', 'fall'), ('spring', 'spring')]
    semester = models.CharField(max_length=6, choices=semesters_choices)
    person = models.ForeignKey(Person, related_name='inactive_semesters')

    def __unicode__(self):
        return u'{} {}: {} {}'.format(self.person.first_name, self.person.last_name, self.semester, self.year)


class DuesPayment(models.Model):
    year = models.IntegerField(max_length=4)
    semesters_choices = [('fall', 'fall'), ('spring', 'spring')]
    semester = models.CharField(max_length=6, choices=semesters_choices)
    person = models.ForeignKey(Person, related_name='dues_payments')

    def __unicode__(self):
        return u'{} {}: {} {}'.format(self.person.first_name, self.person.last_name, self.semester, self.year)


class OverrideRequirement(models.Model):
    year = models.IntegerField(max_length=4)
    semesters_choices = [('fall', 'fall'), ('spring', 'spring')]
    semester = models.CharField(max_length=6, choices=semesters_choices)
    person = models.ForeignKey(Person, related_name='overridden_requirements')
    tours_required = models.IntegerField()
    shifts_required = models.IntegerField()

    def __unicode__(self):
        return u'{} {} {}, {} tours, {} shifts'.format(self.person, self.semester, self.year, self.tours_required, self.shifts_required)
