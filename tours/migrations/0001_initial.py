# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_duespayment_inactivesemester_overriderequirement'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanceledDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DefaultTour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(default=b'Information Office', max_length=500, choices=[(b'Information Office', b'Information Office'), (b"Marshall's Office", b"Marshall's Office"), (b'Alumni Association', b'Alumni Association'), (b'Admissions Office', b'Admissions Office'), (b'Visitas', b'Visitas'), (b"Parents' Weekend", b"Parents' Weekend"), (b'Comp', b'Comp'), (b'Other', b'Other')])),
                ('minute', models.IntegerField(max_length=2)),
                ('hour', models.IntegerField(max_length=2)),
                ('day_num', models.IntegerField(max_length=1)),
                ('notes', models.TextField(max_length=2000, blank=True)),
                ('length', models.IntegerField(default=75, max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InitializedMonth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField(max_length=1)),
                ('year', models.IntegerField(max_length=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenMonth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField(max_length=1)),
                ('year', models.IntegerField(max_length=4)),
                ('opens', models.DateTimeField()),
                ('closes', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(default=b'Information Office', max_length=500)),
                ('time', models.DateTimeField()),
                ('notes', models.TextField(max_length=2000, blank=True)),
                ('missed', models.BooleanField(default=False)),
                ('late', models.BooleanField(default=False)),
                ('length', models.IntegerField(default=75, max_length=3, null=True)),
                ('counts_for_requirements', models.BooleanField(default=True)),
                ('default_tour', models.BooleanField(default=False)),
                ('guide', models.ForeignKey(related_name='tours', blank=True, to='profiles.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
