from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
import vobject

from core import utils as core_utils


class PersonQuerySet(models.QuerySet):
    def inactive(self, semester=None, year=None):
        """
        Includes only members who are inactive for the given semester and year
        """
        if semester is None:
            semester = core_utils.current_semester()
        if year is None:
            year = core_utils.now().year
        else:
            year = int(year)
            semester = semester.lower()

        return self.filter(inactive_semesters__year__exact=year, inactive_semesters__semester=semester)

    def active(self, semester=None, year=None):
        """
        Excludes members who are inactive for the given semester and year
        """
        if semester is None:
            semester = core_utils.current_semester()
        if year is None:
            year = core_utils.now().year
        else:
            year = int(year)

        semester = semester.lower()

        return self.exclude(inactive_semesters__year__exact=year, inactive_semesters__semester=semester)

    def current_members(self, semester=None, year=None):
        if semester is None:
            semester = core_utils.current_semester()
        if year is None:
            year = core_utils.now().year
        else:
            year = int(year)
            semester = semester.lower()

        senior_year, freshman_year = core_utils.class_years(semester=semester, year=year, bookends_only=True)

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

    def requirements(self, semester=None, year=None):
        """
        Get requirements for a given semester.
        """
        year, semester = core_utils.parse_year_semester(year, semester)

        tours_required = self.tours_required_num(semester, year)
        shifts_required = self.shifts_required_num(semester, year)
        dues_required = core_utils.dues_required(semester=semester, year=year)

        return tours_required, shifts_required, dues_required

    def tours_required_num(self, semester=None, year=None):
        year, semester = core_utils.parse_year_semester(year, semester)

        # start with default
        tours_required = core_utils.get_default_num_tours(semester=semester, year=year)

        # check for override
        try:
            overridden_reqs = self.overridden_requirements.get(semester=semester, year=year)
            tours_required = overridden_reqs.tours_required
        except OverrideRequirement.DoesNotExist:
            pass

        # get number of missed tours
        num_missed = self.tours.semester(semester=semester, year=year).filter(missed=True).count()
        num_extra = num_missed * core_utils.get_setting('Missed Tour Penalty')

        return tours_required + num_extra

    def shifts_required_num(self, semester=None, year=None):
        year, semester = core_utils.parse_year_semester(year, semester)

        # start with default
        shifts_required = core_utils.get_default_num_shifts(semester=semester, year=year)

        # check for override
        try:
            overridden_reqs = self.overridden_requirements.get(semester=semester, year=year)
            shifts_required = overridden_reqs.shifts_required
        except OverrideRequirement.DoesNotExist:
            pass

        # get number of missed shifts
        num_missed = self.shifts.semester(semester=semester, year=year).filter(missed=True).count()
        num_extra = num_missed * core_utils.get_setting('Missed Shift Penalty')

        return shifts_required + num_extra

    def dues_status(self, semester=None, year=None):
        year, semester = core_utils.parse_year_semester(year, semester)
        dues_required = core_utils.dues_required(semester=semester, year=year)

        if dues_required:
            if self.dues_payments.filter(year=year, semester=semester):
                return 'complete'
            else:
                return 'incomplete'
        else:
            return 'not_required'

    def tours_status(self, semester=None, year=None):
        """
        Returns dictionary of form:
        {
            'status': 'complete'|'incomplete'|'projected',
            'num_required': int,
            'num_remaining': int,
            'num_to_sign_up': int,
            'num_extra': int,
            'date_projected': date|None,
            'complete': [],
            'late': [],
            'missed': [],
            'upcoming': [],
            'tours': [],
        }
        """
        year, semester = core_utils.parse_year_semester(year, semester)
        now_obj = core_utils.now()
        semester_tours = self.tours.filter(counts_for_requirements=True).semester(semester=semester, year=year).order_by('time')
        complete = semester_tours.filter(missed=False, time__lte=now_obj)
        late = semester_tours.filter(late=True, missed=False, time__lte=now_obj)
        missed = semester_tours.filter(missed=True, time__lte=now_obj)
        past = semester_tours.filter(time__lt=now_obj)
        upcoming = semester_tours.filter(time__gte=now_obj)

        num_required = self.tours_required_num(semester=semester, year=year)
        num_remaining = num_required - complete.count()
        num_extra = abs(min(num_remaining, 0))
        num_remaining = max(num_remaining, 0)
        num_to_sign_up = max(num_remaining - upcoming.count(), 0)

        # calculate status
        if num_remaining <= 0:
            status = 'complete'
        elif num_remaining <= upcoming.count():
            status = 'projected'
        else:
            status = 'incomplete'

        if status == 'projected':
            completion_obj = upcoming[num_remaining - 1]
            date_projected = completion_obj.time
        else:
            date_projected = None

        return {
            'status': status,
            'num_required': num_required,
            'num_remaining': num_remaining,
            'num_to_sign_up': num_to_sign_up,
            'num_extra': num_extra,
            'date_projected': date_projected,
            'complete': complete,
            'late': late,
            'missed': missed,
            'past': past,
            'upcoming': upcoming,
            'tours': semester_tours,
        }

    def shifts_status(self, semester=None, year=None):
        """
        Returns dictionary of form:
        {
            'status': 'complete'|'incomplete'|'projected',
            'num_required': int,
            'num_remaining': int,
            'num_to_sign_up': int,
            'num_extra': int,
            'date_projected': date|None,
            'complete': [],
            'late': [],
            'missed': [],
            'past': [],
            'upcoming': [],
            'shifts': [],
        }
        """
        year, semester = core_utils.parse_year_semester(year, semester)
        now_obj = core_utils.now()
        semester_shifts = self.shifts.filter(counts_for_requirements=True).semester(semester=semester, year=year).order_by('time')
        complete = semester_shifts.filter(missed=False, time__lte=now_obj)
        late = semester_shifts.filter(late=True, missed=False, time__lte=now_obj)
        missed = semester_shifts.filter(missed=True, time__lte=now_obj)
        past = semester_shifts.filter(time__lt=now_obj)
        upcoming = semester_shifts.filter(time__gte=now_obj)

        num_required = self.shifts_required_num(semester=semester, year=year)
        num_remaining = num_required - complete.count()
        num_extra = abs(min(num_remaining, 0))
        num_remaining = max(num_remaining, 0)
        num_to_sign_up = max(num_remaining - upcoming.count(), 0)

        # calculate status
        if num_remaining <= 0:
            status = 'complete'
        elif num_remaining <= upcoming.count():
            status = 'projected'
        else:
            status = 'incomplete'

        if status == 'projected':
            completion_obj = upcoming[num_remaining - 1]
            date_projected = completion_obj.time
        else:
            date_projected = None

        return {
            'status': status,
            'num_required': num_required,
            'num_remaining': num_remaining,
            'num_to_sign_up': num_to_sign_up,
            'num_extra': num_extra,
            'date_projected': date_projected,
            'complete': complete,
            'late': late,
            'missed': missed,
            'past': past,
            'upcoming': upcoming,
            'shifts': semester_shifts,
        }

    def is_active(self, semester=None, year=None):
        if self._default_manager.current_members(semester=semester, year=year).active(semester=semester, year=year).filter(pk=self.pk):
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
        v.tel.value = unicode(self.phone)
        v.tel.type_param = 'MOBILE'
        output = v.serialize()
        return output

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    class Meta:
        permissions = (
            ("send_requirements_email", "Can send requirements emails"),
        )


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
