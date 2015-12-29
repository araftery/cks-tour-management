# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuesPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(max_length=4)),
                ('semester', models.CharField(max_length=6, choices=[(b'fall', b'fall'), (b'spring', b'spring')])),
                ('person', models.ForeignKey(related_name='dues_payments', to='profiles.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InactiveSemester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(max_length=4)),
                ('semester', models.CharField(max_length=6, choices=[(b'fall', b'fall'), (b'spring', b'spring')])),
                ('person', models.ForeignKey(related_name='inactive_semesters', to='profiles.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OverrideRequirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(max_length=4)),
                ('semester', models.CharField(max_length=6, choices=[(b'fall', b'fall'), (b'spring', b'spring')])),
                ('tours_required', models.IntegerField()),
                ('shifts_required', models.IntegerField()),
                ('person', models.ForeignKey(related_name='overridden_requirements', to='profiles.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
