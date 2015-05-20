# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0004_djanguifile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='djanguijob',
            name='celery_state',
        ),
        migrations.AlterField(
            model_name='djanguijob',
            name='status',
            field=models.CharField(default=b'submitted', max_length=255, choices=[(b'submitted', 'Submitted'), (b'running', 'Running'), (b'completed', 'Completed'), (b'deleted', 'Deleted')]),
        ),
    ]
