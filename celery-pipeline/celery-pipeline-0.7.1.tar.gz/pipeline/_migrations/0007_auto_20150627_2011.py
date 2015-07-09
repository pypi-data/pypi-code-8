# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0006_auto_20150627_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventhandler',
            name='criteria',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
