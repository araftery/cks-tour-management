from djang.contrib.auth.models import Group
from django.db.models import Q

from core.utils import now, current_semester


def set_groups_by_position(person):
    """
    Sets permission groups by Board positions, given a user and a position to which they are being
    assigned.
    """
    user = person.user
    position = person.position

    position_groups = Group.objects.filter(Q(name='President') | Q(name='Vice President') | Q(name='Secretary') | Q(name='Treasurer') | Q(name='Tour Coordinators') | Q(name='Board Members'))

    # remove from existing position groups
    for group in position_groups:
        user.groups.remove(group)

    position_to_groups = {
        'President': ('President', 'Board Members',),
        'Vice President': ('Vice President', 'Board Members',),
        'Secretary': ('Secretary', 'Board Members',),
        'Treasurer': ('Treasurer', 'Board Members',),
        'Tour Coordinator (Primary)': ('Tour Coordinators', 'Board Members',),
        'Tour Coordinator': ('Tour Coordinators', 'Board Members',),
        'Treasurer': ('Treasurer', 'Board Members',),
        'Freshman Week Coordinator': ('Freshman Week Coordinators', 'Board Members',),
        'Other Board Member': ('Board Members',),
    }

    for group in position_to_groups[position]:
        Group.objects.get(name=group).user_set.add(user)


def member_latest_semester(person):
    """
    Finds the latest semester a member was in Crimson Key. For graduated members,
    this means the spring of their senior year. Otherwise, it's usually latest semester
    (as in current_semester()).

    Raises a ValueError if something goes wrong (e.g., a person in the db is not yet a member,
    i.e. member_since > current year).
    """
    member_since = person.member_since
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
