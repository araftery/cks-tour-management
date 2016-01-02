from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Q

from celery.task import task
from core.utils import now, current_semester, get_setting, send_email, dues_required
from profiles.models import Person


def set_groups_by_position(person):
    """
    Sets permission groups by Board positions, given a user and a position to which they are being
    assigned.
    """
    user = person.user
    position = person.position

    position_groups = Group.objects.filter(Q(name='President') | Q(name='Vice President') | Q(name='Secretary') | Q(name='Treasurer') | Q(name='Freshman Week Coordinators') | Q(name='Tour Coordinators') | Q(name='Board Members'))

    # remove from existing position groups
    for group in position_groups:
        user.groups.remove(group)

    position_to_groups = {
        'President': ('President',),
        'Vice President': ('Vice President',),
        'Secretary': ('Secretary',),
        'Treasurer': ('Treasurer',),
        'Tour Coordinator (Primary)': ('Tour Coordinators',),
        'Tour Coordinator': ('Tour Coordinators',),
        'Treasurer': ('Treasurer',),
        'Freshman Week Coordinator': ('Freshman Week Coordinators',),
        'Other Board Member': (),
    }

    try:
        for group in position_to_groups[position]:
            Group.objects.get(name=group).user_set.add(user)
    except KeyError:
        # position has no defined groups
        pass

    if position in settings.BOARD_POSITIONS:
        Group.objects.get(name='Board Members').user_set.add(user)


def member_latest_semester(person):
    """
    Finds the latest semester a member was in Crimson Key. For graduated members,
    this means the spring of their senior year. Otherwise, it's usually latest semester
    (as in current_semester()).

    Raises a ValueError if something goes wrong (e.g., a person in the db is not yet a member,
    i.e. member_since > current year).
    """
    member_since = person.member_since_year
    grad_year = person.year

    semester = current_semester()
    year = now().year

    latest_semester = None
    latest_year = None

    if semester == 'fall':

        # if has graduated, return spring of their grad year
        if year >= grad_year:
            latest_semester = 'spring'
            latest_year = grad_year

        # if hasn't graduated
        else:
            if member_since > year:
                latest_semester = semester
                latest_year = member_since
            else:
                latest_semester = semester
                latest_year = year

    elif semester == 'spring':

        # if has graduated, return spring of their grad year
        if year > grad_year:
            latest_semester = 'spring'
            latest_year = grad_year

        # if hasn't graduated
        else:
            if member_since >= year:
                latest_semester = semester
                latest_year = member_since
            else:
                latest_semester = semester
                latest_year = year

    return latest_year, latest_semester


def get_person_by_position(*positions):
    """
    Return first Person found at the given positions, else None.
    """
    ret = None
    for position in positions:
        person = Person.objects.filter(position=position).order_by('pk').first()
        if person is not None:
            ret = person
            break
    return ret


def get_email_by_position(*positions):
    """
    Return email of first person at position, falls back on fallback email address.
    """
    person = get_person_by_position(*positions)
    fallback = get_setting('Fallback Email Address')
    return '{} {} <{}>'.format(person.first_name, person.last_name, person.email) if person is not None else fallback


@task
def send_requirements_email(person):
    from_person = get_person_by_position('Secretary')
    if from_person is None:
        signature = 'Crimson Key Society'
    else:
        signature = from_person.first_name

    from_email = get_email_by_position('Secretary')
    to_emails = ['{} <{}>'.format(person.full_name, person.email)]

    subject = 'Crimson Key Requirements Update'

    dues_status = person.dues_status()
    person.cached_status = {
        'tours_status': person.tours_status(),
        'shifts_status': person.shifts_status(),
        'dues_status': dues_status,
    }
    collect_dues = dues_required()

    context = {'person': person, 'collect_dues': collect_dues, 'dues_required': dues_required, 'signature': signature}
    send_email(subject, to_emails, from_email, 'email/requirements_email.txt', 'email/requirements_email.html', context)
