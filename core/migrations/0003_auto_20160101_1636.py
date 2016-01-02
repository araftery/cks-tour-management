# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151231_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='value_type',
            field=models.CharField(max_length=50, choices=[(b'int', b'int'), (b'float', b'float'), (b'string', b'string'), (b'bool', b'bool'), (b'email', b'email'), (b'semester_or_never', b'semester_or_never')]),
            preserve_default=True,
        ),
    ]
