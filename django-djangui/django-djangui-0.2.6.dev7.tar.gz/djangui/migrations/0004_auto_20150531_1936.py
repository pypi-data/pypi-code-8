# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangui', '0003_auto_20150531_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='djanguifile',
            name='filepath',
            field=models.FileField(upload_to='', max_length=500),
        ),
        migrations.AlterField(
            model_name='djanguijob',
            name='status',
            field=models.CharField(default='submitted', choices=[('submitted', 'Submitted'), ('running', 'Running'), ('completed', 'Completed'), ('deleted', 'Deleted')], max_length=255),
        ),
        migrations.AlterField(
            model_name='script',
            name='save_path',
            field=models.CharField(null=True, blank=True, max_length=255, help_text='By default save to the script name, this will change the output folder.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='script_path',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='script',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, populate_from='script_name', editable=False),
        ),
        migrations.AlterField(
            model_name='scriptgroup',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, populate_from='group_name', editable=False),
        ),
        migrations.AlterField(
            model_name='scriptparameter',
            name='param_help',
            field=models.TextField(null=True, blank=True, verbose_name='help'),
        ),
        migrations.AlterField(
            model_name='scriptparameter',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, populate_from='script_param', editable=False),
        ),
        migrations.AlterField(
            model_name='scriptparameters',
            name='_value',
            field=models.TextField(db_column='value'),
        ),
    ]
