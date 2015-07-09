# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0005_auto_20150627_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventHandler',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('events', jsonfield.fields.JSONField(default=[])),
                ('criteria', jsonfield.fields.JSONField(default=[])),
                ('actions', jsonfield.fields.JSONField()),
                ('app_name', models.CharField(max_length=64, blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Configuration',
        ),
    ]
