# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_auto_20150514_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='additional',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
