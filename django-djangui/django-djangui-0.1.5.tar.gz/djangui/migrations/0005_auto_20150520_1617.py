# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0004_djanguijob_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjanguiFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filepath', models.FileField(upload_to=b'')),
                ('filepreview', models.TextField(null=True, blank=True)),
                ('filetype', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='djanguijob',
            name='celery_state',
        ),
        migrations.AlterField(
            model_name='djanguijob',
            name='status',
            field=models.CharField(default=b'submitted', max_length=255, choices=[(b'submitted', 'Submitted'), (b'running', 'Running'), (b'completed', 'Completed'), (b'deleted', 'Deleted')]),
        ),
        migrations.AddField(
            model_name='djanguifile',
            name='job',
            field=models.ForeignKey(to='djangui.DjanguiJob'),
        ),
        migrations.AddField(
            model_name='djanguifile',
            name='parameter',
            field=models.ForeignKey(blank=True, to='djangui.ScriptParameters', null=True),
        ),
    ]
