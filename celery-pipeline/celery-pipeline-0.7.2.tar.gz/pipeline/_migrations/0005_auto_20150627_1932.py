# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0004_auto_20150530_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configurationsource',
            old_name='source_class',
            new_name='event',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='source',
        ),
        migrations.AddField(
            model_name='configuration',
            name='criteria',
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='configuration',
            name='events',
            field=jsonfield.fields.JSONField(default=[]),
        ),
    ]
