# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

from django.db import migrations

from core.utils import now


defaults = OrderedDict((
    ('Tours Required', {
        'description': 'Number of tours required per semester.',
        'value_type': 'int',
        'value': '2',
    }),
    ('Shifts Required', {
        'description': 'Number of shifts required per semester.',
        'value_type': 'int',
        'value': '1',
    }),
    ('Send Email Reminders', {
        'description': 'true if email reminders should be sent before tours and shifts, false if not.',
        'value_type': 'bool',
        'value': 'true',
    }),
    ('Send Shift Reminders', {
        'description': 'true if text reminders should be sent before tours and shifts, false if not.',
        'value_type': 'bool',
        'value': 'true',
    }),
    ('Info Center Director Name', {
        'description': 'Name of the person who Key members should call or text if they are running late for a tour.',
        'value_type': 'string',
        'value': 'Kendyl',
    }),
    ('Info Center Phone Number', {
        'description': 'Phone number which Key members should call or text if they are running late for a tour.',
        'value_type': 'string',
        'value': '555-555-5555',
    }),
    ('Allow Texting to Info Center', {
        'description': 'If true, Key members will be instructed to call or text the number above if they are running late for a tour. If false, they will be instructed only to call. Set to false if the phone number above does not accept texts (for example, the Info Center landline).',
        'value_type': 'bool',
        'value': 'true',
    }),
    ('Collect Dues', {
        'description': 'Semester when dues are collected. Can be: fall, spring, both, or never.',
        'value_type': 'semester_or_never',
        'value': 'fall',
    }),
    ('Missed Tour Penalty', {
        'description': 'Number of extra tours required if a tour is missed.',
        'value_type': 'int',
        'value': '1',
    }),
    ('Missed Shift Penalty', {
        'description': 'Number of extra shifts required if a shift is missed.',
        'value_type': 'int',
        'value': '1',
    }),
    ('Fallback Email Address', {
        'description': 'Email address from which to send emails if the appropriate board member cannot be found.',
        'value_type': 'email',
        'value': 'crimsonkeysociety@gmail.com',
    }),
    ('Twilio Account SID', {
        'description': 'Twilio API account SID for sending text reminders.',
        'value_type': 'string',
        'value': '12456',
    }),
    ('Twilio Auth Token', {
        'description': 'Twilio API auth token for sending text reminders.',
        'value_type': 'string',
        'value': '12456',
    }),
    ('Twilio Phone Number', {
        'description': "Crimson Key's Twilio phone number for sending text reminders. Should start with +1 and have no other punctuation.",
        'value_type': 'string',
        'value': '+15555555555',
    }),
))


def create_default_settings(apps, schema_editor):
    """
    Creates some default settings that other apps rely on.
    If a setting already exists, leaves them be.

    Defaults are based on Fall 2015 values.
    """
    Setting = apps.get_model("core", "Setting")

    now_obj = now()

    # make sure we don't collide with current order nums
    current_order_nums = set([x.order_num for x in Setting.objects.all()])

    for order_num, name in enumerate(defaults):
        while order_num in current_order_nums:
            order_num += 1

        current_order_nums.add(order_num)

        if not Setting.objects.filter(name=name):
            Setting.objects.create(name=name, time_set=now_obj, order_num=order_num, **defaults[name])


def reverse_create_default_settings(apps, schema_editor):
    Setting = apps.get_model("core", "Setting")

    for name in defaults:
        Setting.objects.filter(name=name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_settings, reverse_create_default_settings)
    ]
