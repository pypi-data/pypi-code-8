# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0012_auto_20150113_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='current_metadata',
            field=django_pgjson.fields.JsonBField(blank=True, default=None, null=True),
            preserve_default=True,
        ),
    ]
