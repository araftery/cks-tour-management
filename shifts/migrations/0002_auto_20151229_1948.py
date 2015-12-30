# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='person',
            field=models.ForeignKey(related_name='shifts', blank=True, to='profiles.Person', null=True),
            preserve_default=True,
        ),
    ]
