# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0010_auto_20140827_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentrevision',
            name='data_delete_point',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='componentattribute',
            name='parent',
            field=models.ForeignKey(to='mirrors.Component', related_name='attributes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='componentlock',
            name='component',
            field=models.ForeignKey(to='mirrors.Component', related_name='locks'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='componentrevision',
            name='component',
            field=models.ForeignKey(to='mirrors.Component', related_name='revisions'),
            preserve_default=True,
        ),
    ]
