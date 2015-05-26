# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0005_auto_20150520_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='djanguifile',
            name='filepath',
            field=models.FileField(max_length=500, upload_to=b''),
        ),
    ]
