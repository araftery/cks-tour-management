# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


groups = {
    'President': (
        'tours.Tour',
        'tours.CanceledDay',
        'tours.DefaultTour',
        'tours.InitializedMonth',
        'tours.OpenMonth',
        'profiles.DuesPayment',
        'profiles.InactiveSemester',
        'profiles.OverrideRequirement',
        'profiles.Person',
        'core.Setting',
        'auth.User',
        'auth.Group',
    ),
    'Vice President': (
        'tours.Tour',
        'tours.CanceledDay',
        'tours.DefaultTour',
        'tours.InitializedMonth',
        'tours.OpenMonth',
        'profiles.DuesPayment',
        'profiles.InactiveSemester',
        'profiles.OverrideRequirement',
        'profiles.Person',
        'core.Setting',
        'auth.User',
        'auth.Group',
    ),
    'Treasurer': (
        'profiles.DuesPayment',
    ),
    'Secretary': (
        'tours.Tour',
        'profiles.DuesPayment',
        'profiles.InactiveSemester',
        'profiles.OverrideRequirement',
        'profiles.Person',
        'core.Setting',
        'auth.User',
        'auth.Group',
    ),
    'Tour Coordinators': (
        'tours.Tour',
        'tours.CanceledDay',
        'tours.DefaultTour',
        'tours.InitializedMonth',
        'tours.OpenMonth',
        'core.Setting',
    ),
    'Freshman Week Coordinators': (
        'tours.Tour',
        'shifts.Shift',
    ),
    'Board Members': (
        'shifts.Shift',
    ),
}


def create_auth_groups(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    Group = apps.get_model("auth", "Group")

    for group_name, model_names in groups.iteritems():
        content_types = [ContentType.objects.get(app_label=model_name.rsplit('.', 1)[0], model=model_name.rsplit('.', 1)[1].lower()) for model_name in model_names]
        group, created = Group.objects.get_or_create(name=group_name)
        for content_type in content_types:
            permissions = Permission.objects.filter(content_type=content_type)
            for permission in permissions:
                group.permissions.add(permission)


def reverse_create_auth_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=groups.keys()).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160101_1636'),
        ('shifts', '0002_auto_20151229_1948'),
        ('tours', '0003_auto_20160101_1636'),
        ('profiles', '0003_auto_20160101_1636'),
        ('default', '0003_alter_email_max_length'),
    ]

    operations = [
        migrations.RunPython(create_auth_groups, reverse_create_auth_groups)
    ]
