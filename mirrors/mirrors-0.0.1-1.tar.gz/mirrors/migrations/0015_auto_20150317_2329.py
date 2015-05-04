# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields
import mirrors.models


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0014_auto_20150224_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='componentrevision',
            name='metadata_tmp',
        ),
        migrations.AlterField(
            model_name='component',
            name='month',
            field=models.IntegerField(default=0, validators=[mirrors.models.validate_is_month], null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='component',
            name='year',
            field=models.IntegerField(default=0, validators=[mirrors.models.validate_is_year], null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='componentrevision',
            name='metadata',
            field=django_pgjson.fields.JsonBField(blank=True, default=None, null=True),
            preserve_default=True,
        ),
    ]
