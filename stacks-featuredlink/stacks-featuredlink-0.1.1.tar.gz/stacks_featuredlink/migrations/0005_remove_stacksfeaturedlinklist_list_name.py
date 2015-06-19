# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_featuredlink', '0004_auto_20150528_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stacksfeaturedlinklist',
            name='list_name',
        ),
    ]
