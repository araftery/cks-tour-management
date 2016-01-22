import json

from django.contrib.auth.models import User
from django.db.models.loading import get_model

from social.apps.django_app.default.models import UserSocialAuth

from profiles.models import Person
from profiles.utils import set_groups_by_position

for x in (User, Person, UserSocialAuth):
    x.objects.all().delete()


# members
with open('serialized_objects/person.json', 'r') as infile:
    objects = json.load(infile)

for obj in objects:
    kwargs = {}
    kwargs['pk'] = obj['pk']
    kwargs.update(obj['fields'])
    del kwargs['user']
    person = Person.objects.create(**kwargs)
    username = person.harvard_email.split('@')[0]
    user = User.objects.create_user(username=username, email=person.harvard_email, first_name=person.first_name, last_name=person.last_name)

    # no need for the user to have a password, since we'll use Google OAuth to login
    user.set_unusable_password()
    user.save()

    person.user = user
    person.save()

    UserSocialAuth.objects.create(user=user, provider='google-oauth2', uid=person.harvard_email)

    # set appropriate groups and status based on position
    set_groups_by_position(person)

    if person.site_admin is True:
        user.is_staff = True
        user.is_superuser = True
        user.save()


easy_modules = ['canceledday', 'duespayment', 'inactivesemester', 'initializedmonth', 'openmonth', 'overriderequirement', 'shifts', 'tours']

for mod in easy_modules:
    with open('serialized_objects/{}.json'.format(mod), 'r') as infile:
        objects = json.load(infile)

    model = get_model(*objects[0]['model'].split('.'))

    model.objects.all().delete()

    for obj in objects:
        try:
            obj['fields']['guide'] = Person.objects.get(pk=obj['fields']['guide'])
        except:
            pass

        try:
            obj['fields']['person'] = Person.objects.get(pk=obj['fields']['person'])
        except:
            pass

        model.objects.create(pk=obj['pk'], **obj['fields'])
