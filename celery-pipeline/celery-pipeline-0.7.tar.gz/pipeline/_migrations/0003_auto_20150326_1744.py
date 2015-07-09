# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0002_configuration_app_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='app_name',
            field=models.CharField(max_length=64, blank=True, null=True),
            preserve_default=True,
        ),
    ]
