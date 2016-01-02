# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0002_auto_20151229_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaulttour',
            name='day_num',
            field=models.IntegerField(max_length=1, choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')]),
            preserve_default=True,
        ),
    ]
