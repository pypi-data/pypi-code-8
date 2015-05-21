# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0003_auto_20150507_0347'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjanguiFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filepath', models.FileField(upload_to=b'')),
                ('filepreview', models.TextField(null=True, blank=True)),
                ('filetype', models.CharField(max_length=255, null=True, blank=True)),
                ('job', models.ForeignKey(to='djangui.DjanguiJob')),
                ('parameter', models.ForeignKey(blank=True, to='djangui.ScriptParameters', null=True)),
            ],
        ),
    ]
