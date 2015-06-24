# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def populate_display_title(apps, schema_editor):
    """
    Populates display_title on both StacksFeaturedLink and
    StacksFeaturedLinkList.
    """
    StacksFeaturedLink = apps.get_model(
        "stacks_featuredlink", "StacksFeaturedLink"
    )
    for link in StacksFeaturedLink.objects.all():
        link.display_title = link.name
        link.save()

    StacksFeaturedLinkList = apps.get_model(
        "stacks_featuredlink", "StacksFeaturedLinkList"
    )
    for link_list in StacksFeaturedLinkList.objects.all():
        link_list.name = link_list.list_name
        link_list.display_title = link_list.list_name
        link_list.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_featuredlink', '0003_auto_20150528_1559'),
    ]

    operations = [
        migrations.RunPython(
            populate_display_title,
        )
    ]
