# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoker', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('response', models.IntegerField()),
                ('ip', models.IPAddressField()),
                ('additional', models.CharField(max_length=255)),
            ],
        ),
    ]
