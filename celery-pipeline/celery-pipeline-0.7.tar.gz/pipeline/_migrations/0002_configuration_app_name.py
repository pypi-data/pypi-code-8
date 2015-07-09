# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='app_name',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
    ]
