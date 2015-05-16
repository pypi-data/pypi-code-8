# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_auto_20150514_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 14, 21, 58, 1, 686000), auto_now_add=True),
            preserve_default=False,
        ),
    ]
