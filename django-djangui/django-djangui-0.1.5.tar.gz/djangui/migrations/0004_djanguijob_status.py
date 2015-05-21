# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0003_auto_20150505_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='djanguijob',
            name='status',
            field=models.CharField(default=b'submitted', max_length=10, choices=[(b'submitted', 'Submitted'), (b'completed', 'Completed'), (b'deleted', 'Deleted')]),
        ),
    ]
