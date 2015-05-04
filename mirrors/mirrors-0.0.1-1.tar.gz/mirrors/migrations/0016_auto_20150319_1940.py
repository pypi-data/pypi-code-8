# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mirrors.models


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0015_auto_20150317_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='month',
            field=models.IntegerField(null=True, validators=[mirrors.models.validate_is_month], default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='component',
            name='year',
            field=models.IntegerField(null=True, validators=[mirrors.models.validate_is_year], default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='componentattribute',
            name='child',
            field=models.ForeignKey(null=True, to='mirrors.Component', blank=True),
            preserve_default=True,
        ),
    ]
