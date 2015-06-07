# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('slug', models.CharField(
                    unique=True,
                    max_length=255,
                    verbose_name='slug')),
                ('data', models.TextField(
                    verbose_name='content')),
                ('specs', models.TextField(
                    default=b'',
                    verbose_name='specification')),
            ],
            options={
                'verbose_name': 'template',
                'verbose_name_plural': 'templates',
            },
        ),
    ]
