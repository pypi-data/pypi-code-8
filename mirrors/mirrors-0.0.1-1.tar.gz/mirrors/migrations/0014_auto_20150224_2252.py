# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import models, migrations
import django_pgjson.fields


def forwards_func(apps, schema_editor):
    ComponentRevision = apps.get_model('mirrors', 'ComponentRevision')
    db_alias = schema_editor.connection.alias

    for rev in ComponentRevision.objects.all():
        rev.metadata_tmp = json.loads(rev.metadata)
        rev.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0013_auto_20150127_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='componentrevision',
            name='metadata_tmp',
            field=django_pgjson.fields.JsonBField(blank=True, default=None, null=True),
            preserve_default=True,
        ),
        migrations.RunPython(code=forwards_func),
        migrations.RunSQL(
            sql='ALTER TABLE mirrors_componentrevision DROP COLUMN metadata',
            state_operations=[migrations.RemoveField('component', 'metadata')]
        ),
        migrations.RunSQL(
            sql='ALTER TABLE mirrors_componentrevision RENAME COLUMN metadata_tmp TO metadata',
            state_operations=[migrations.RenameField('component', 'metadata_tmp', 'metadata')]
        ),
        # this hides the fact that we were playing weird games with the columns
        migrations.RunSQL(
            sql='ALTER TABLE mirrors_componentrevision ADD COLUMN metadata_tmp text'),
    ]
