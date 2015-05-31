# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_renderit_plugin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='renderitcmsplugin',
            name='tag_libraries',
            field=models.CharField(blank=True, default='', max_length=255,
                                   help_text='Custom tag libraries, space-separated'),
            preserve_default=True,
        ),
    ]
