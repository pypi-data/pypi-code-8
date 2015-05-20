# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0005_auto_20150510_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptparameter',
            name='output_path',
            field=models.FilePathField(path=b'/home/chris/Devel/newproj/newproj/user_uploads', max_length=255, allow_files=False, recursive=True, allow_folders=True),
        ),
    ]
