# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_textblock', '0004_auto_20150528_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stackstextblocklist',
            name='list_name',
        ),
        migrations.AlterField(
            model_name='stackstextblock',
            name='display_title',
            field=models.CharField(help_text='An optional displayed-to-the-user title of this content.', max_length=100, verbose_name='Display Title', blank=True),
        ),
        migrations.AlterField(
            model_name='stackstextblocklist',
            name='display_title',
            field=models.CharField(help_text='An optional displayed-to-the-user title of this content.', max_length=100, verbose_name='Display Title', blank=True),
        ),
    ]
