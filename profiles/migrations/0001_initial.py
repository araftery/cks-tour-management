# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=75)),
                ('harvard_email', models.EmailField(max_length=75)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('year', models.IntegerField(max_length=4)),
                ('notes', models.TextField(max_length=2000, blank=True)),
                ('position', models.CharField(default=b'Regular Member', max_length=50, choices=[(b'President', b'President'), (b'Vice President', b'Vice President'), (b'Treasurer', b'Treasurer'), (b'Secretary', b'Secretary'), (b'Tour Coordinator (Primary)', b'Tour Coordinator (Primary)'), (b'Tour Coordinator', b'Tour Coordinator'), (b'Freshman Week Coordinator', b'Freshman Week Coordinator'), (b'Other Board Member', b'Other Board Member'), (b'Regular Member', b'Regular Member')])),
                ('site_admin', models.BooleanField(default=False)),
                ('member_since_year', models.IntegerField(max_length=4)),
                ('house', models.CharField(blank=True, max_length=50, null=True, choices=[(b'Adams', b'Adams'), (b'Quincy', b'Quincy'), (b'Lowell', b'Lowell'), (b'Eliot', b'Eliot'), (b'Kirkland', b'Kirkland'), (b'Winthrop', b'Winthrop'), (b'Mather', b'Mather'), (b'Leverett', b'Leverett'), (b'Dunster', b'Dunster'), (b'Cabot', b'Cabot'), (b'Pforzheimer', b'Pforzheimer'), (b'Currier', b'Currier'), (b'Dudley', b'Dudley'), (b'Freshman (Yard)', b'Freshman (Yard)')])),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
