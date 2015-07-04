# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to='logos/', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires_on', models.DateTimeField(default=datetime.datetime(2016, 7, 4, 11, 1, 13, 352122))),
                ('does_expire', models.BooleanField(default=False)),
                ('type', models.PositiveIntegerField(default=0, blank=True, choices=[(0, 'NONE'), (1, 'PLATINUM'), (2, 'GOLD'), (3, 'SILVER'), (4, 'BRONCE')])),
                ('width', models.PositiveIntegerField(default=200, blank=True)),
                ('height', models.PositiveIntegerField(default=None, null=True, blank=True)),
            ],
        ),
    ]
