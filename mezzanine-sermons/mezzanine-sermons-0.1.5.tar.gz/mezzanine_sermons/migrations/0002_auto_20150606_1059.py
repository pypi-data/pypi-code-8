# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_sermons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sermon',
            name='preacher',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
