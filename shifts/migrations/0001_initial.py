# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_duespayment_inactivesemester_overriderequirement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=500)),
                ('time', models.DateTimeField()),
                ('notes', models.TextField(max_length=2000, blank=True)),
                ('missed', models.BooleanField(default=False)),
                ('late', models.BooleanField(default=False)),
                ('length', models.IntegerField(max_length=3, null=True, blank=True)),
                ('counts_for_requirements', models.BooleanField(default=True)),
                ('person', models.ForeignKey(related_name='shifts', to='profiles.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
