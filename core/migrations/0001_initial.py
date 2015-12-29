# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('value', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('time_set', models.DateTimeField()),
                ('order_num', models.IntegerField()),
                ('value_type', models.CharField(max_length=50, choices=[(b'int', b'int'), (b'float', b'float'), (b'string', b'string'), (b'bool', b'bool'), (b'email', b'email'), (b'semester_or_none', b'semester_or_none')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
