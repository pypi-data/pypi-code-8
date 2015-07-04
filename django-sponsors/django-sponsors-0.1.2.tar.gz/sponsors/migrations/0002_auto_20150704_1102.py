# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sponsor',
            old_name='type',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 4, 11, 2, 5, 161870)),
        ),
    ]
