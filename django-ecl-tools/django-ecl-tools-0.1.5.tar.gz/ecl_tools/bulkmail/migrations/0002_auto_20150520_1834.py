# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulkmail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='optin',
            name='signup_ip_address',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='optin',
            name='signup_uri',
            field=models.URLField(max_length=300, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='optin',
            name='verified',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='optin',
            name='verified_ip_address',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
