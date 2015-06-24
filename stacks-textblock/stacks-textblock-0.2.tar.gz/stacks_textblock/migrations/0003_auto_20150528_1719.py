# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_textblock', '0002_auto_20150407_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stackstextblocklisttextblock',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='stackstextblocklisttextblock',
            name='date_modified',
        ),
        migrations.AddField(
            model_name='stackstextblock',
            name='display_title',
            field=models.CharField(default='Foo', help_text='The displayed-to-the-user title of this content.', max_length=100, verbose_name='Display Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stackstextblocklist',
            name='display_title',
            field=models.CharField(default='Foo', help_text='The displayed-to-the-user title of this content.', max_length=100, verbose_name='Display Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stackstextblocklist',
            name='name',
            field=models.CharField(default='Foo', help_text='The internal name/signifier of this content.', max_length=100, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stackstextblock',
            name='name',
            field=models.CharField(help_text='The internal name/signifier of this content.', max_length=100, verbose_name='Name'),
        ),
    ]
