# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_snippet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='display_title',
            field=models.CharField(help_text='An optional displayed-to-the-user title of this content.', max_length=100, verbose_name='Display Title', blank=True),
        ),
    ]
