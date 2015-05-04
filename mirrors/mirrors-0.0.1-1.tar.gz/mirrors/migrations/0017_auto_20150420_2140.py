# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import models, migrations


def combine_YYYYMM(apps, schema_editor):
    Component = apps.get_model('mirrors', 'Component')
    for component in Component.objects.all():
        if component.year is not None and component.month is not None:
            component.slug = "{0:04d}-{1:02d}-{2!s}".format(component.year,
                                                            component.month,
                                                            component.slug)
            component.save()


def split_YYYYMM(apps, schema_editor):
    split_p_regexp = r'^(\d{4})-(\d{2)}-([a-zA-Z]+)$'
    split_p = re.compile(split_p_regexp)

    Component = apps.get_model('mirrors', 'Component')

    for component in Component.objects.filter(slug__regex=split_p):
        m = split_p.match(component.slug)

        try:
            component.year = int(m.group(0))
            component.month = int(m.group(1))
            component.slug = m.group(2)
        except ValueError:
            print("Unable to split the slug for component {}".format(
                component.slug))

        component.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0016_auto_20150319_1940'),
    ]

    operations = [
        migrations.RunPython(code=combine_YYYYMM,
                             reverse_code=split_YYYYMM),
        migrations.AlterField(
            model_name='component',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='component',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='component',
            name='month',
        ),
        migrations.RemoveField(
            model_name='component',
            name='year',
        ),
    ]
