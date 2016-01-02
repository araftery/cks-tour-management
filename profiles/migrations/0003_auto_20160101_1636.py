# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_duespayment_inactivesemester_overriderequirement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': (('send_requirements_email', 'Can send requirements emails'),)},
        ),
    ]
