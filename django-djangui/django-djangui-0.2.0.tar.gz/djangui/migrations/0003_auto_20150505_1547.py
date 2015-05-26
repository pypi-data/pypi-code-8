# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0002_auto_20150504_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptparameter',
            name='param_help',
            field=models.TextField(null=True, verbose_name=b'help', blank=True),
        ),
    ]
