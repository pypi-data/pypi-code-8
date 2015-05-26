# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0002_auto_20150506_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='djanguijob',
            name='status',
            field=models.CharField(default=b'submitted', max_length=10, choices=[(b'submitted', 'Submitted'), (b'completed', 'Completed'), (b'deleted', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='scriptparameter',
            name='output_path',
            field=models.FilePathField(path=b'/home/chris/Devel/djtest/djtest/user_uploads', max_length=255, allow_files=False, recursive=True, allow_folders=True),
        ),
    ]
