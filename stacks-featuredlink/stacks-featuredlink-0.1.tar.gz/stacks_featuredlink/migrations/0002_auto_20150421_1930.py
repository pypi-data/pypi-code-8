# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_featuredlink', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stacksfeaturedlinklist',
            options={'verbose_name': 'Stacks Featured Link List', 'verbose_name_plural': 'Stacks Featured Link Lists'},
        ),
        migrations.AlterField(
            model_name='stacksfeaturedlink',
            name='url',
            field=models.URLField(max_length=300, verbose_name='URL', blank=True),
            preserve_default=True,
        ),
    ]
