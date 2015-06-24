# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_content_authors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contenttranslation',
            options={'permissions': (('list_contents', 'Can list all content'),)},
        ),
    ]
