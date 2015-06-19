# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def populate_display_title(apps, schema_editor):
    """
    Populates display_title on both StacksTextBlock and StacksTextBlockList
    """
    StacksTextBlock = apps.get_model(
        "stacks_textblock", "StacksTextBlock"
    )
    for textblock in StacksTextBlock.objects.all():
        textblock.display_title = textblock.name
        textblock.save()

    StacksTextBlockList = apps.get_model(
        "stacks_textblock", "StacksTextBlockList"
    )
    for textblock_list in StacksTextBlockList.objects.all():
        textblock_list.name = textblock_list.list_name
        textblock_list.display_title = textblock_list.list_name
        textblock_list.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_textblock', '0003_auto_20150528_1719'),
    ]

    operations = [
        migrations.RunPython(
            populate_display_title,
        )
    ]
