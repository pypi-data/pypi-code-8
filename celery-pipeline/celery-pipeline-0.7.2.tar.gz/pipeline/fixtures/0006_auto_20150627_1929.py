# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0005_rename_source_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='source',
        ),
        migrations.RemoveField(
            model_name='configurationsource',
            name='source_class',
        ),
        migrations.AddField(
            model_name='configuration',
            name='criteria',
            field=jsonfield.fields.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuration',
            name='events',
            field=jsonfield.fields.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configurationsource',
            name='event',
            field=models.CharField(max_length=255, default=[]),
            preserve_default=False,
        ),
    ]
