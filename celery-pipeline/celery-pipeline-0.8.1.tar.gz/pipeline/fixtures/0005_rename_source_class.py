# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0004_auto_20150530_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='source_class',
            new_name='event',
        ),
    ]
