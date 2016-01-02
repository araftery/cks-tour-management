import datetime

from django.conf import settings

from core.models import Setting
from core.setting_validators import setting_validators
from core.utils.date import now, current_semester


def get_setting(name, semester=None, year=None, time=None):
    """
    Gets the setting value at the given time.
    """
    if time is not None:
        pass
    elif semester is not None and year is not None:
        # get time object for end of semester
        if semester == 'spring':
            month, day = settings.SPRING_SEMESTER_END
        elif semester == 'fall':
            month, day = settings.FALL_SEMESTER_END
        else:
            raise ValueError

        time = datetime.datetime(year, month, day)
    else:
        time = now()

    try:
        setting = Setting.objects.filter(name=name, time_set__lte=time).latest('time_set')
    except Setting.DoesNotExist:
        # if it doesn't exist for that time, just get the latest value
        setting = Setting.objects.filter(name=name).latest('time_set')

    if setting is None:
        raise ValueError('Setting {} does not exist.'.format(name))

    cleaned_value = setting_validators[setting.value_type](setting.value)['value']

    return cleaned_value


def get_default_num_tours(semester=None, year=None, time=None):
    return get_setting(name='Tours Required', semester=semester, year=year, time=time)


def get_default_num_shifts(semester=None, year=None, time=None):
    return get_setting(name='Shifts Required', semester=semester, year=year, time=time)


def dues_required(semester=None, year=None, time=None):
    dues_required_semester = get_setting(name='Collect Dues')
    if time is None and semester is None:
        time = now()

    if time:
        semester = current_semester(time)

    return dues_required_semester == 'both' or dues_required_semester == semester
