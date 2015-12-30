# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initializedmonth',
            name='month',
            field=models.IntegerField(max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='openmonth',
            name='month',
            field=models.IntegerField(max_length=2),
            preserve_default=True,
        ),
    ]
