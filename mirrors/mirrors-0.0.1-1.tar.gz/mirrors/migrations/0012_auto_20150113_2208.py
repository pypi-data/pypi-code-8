# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0011_auto_20141103_2224'),
    ]

    operations = [
        migrations.RunSQL("""
        ALTER TABLE mirrors_componentrevision
        ALTER COLUMN metadata SET DATA TYPE json USING metadata::json,
        ALTER COLUMN metadata SET DEFAULT '{}'::json;
        """)
    ]
