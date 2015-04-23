# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geohash_date', models.DateField(unique=True, verbose_name=b'date')),
                ('djia_open', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('latitude_delta', models.CharField(max_length=30, null=True, blank=True)),
                ('longitude_delta', models.CharField(max_length=30, null=True, blank=True)),
                ('djia_open_30w_adj', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('latitude_delta_30w_adj', models.CharField(max_length=30, null=True, blank=True)),
                ('longitude_delta_30w_adj', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'ordering': ('geohash_date',),
            },
            bases=(models.Model,),
        ),
    ]
