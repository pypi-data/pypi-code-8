# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sermon',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=60)),
                ('passage', models.CharField(max_length=100, help_text='The bible passage for the individual sermon', blank=True)),
                ('preacher', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('audio', mezzanine.core.fields.FileField(max_length=255, verbose_name='The audio file', help_text='Select the audio file using the file manager (Only .mp3 files accepted)', blank=True)),
            ],
            options={
                'verbose_name': 'Individual Sermon',
                'ordering': ['-date'],
                'verbose_name_plural': 'Individual Sermons',
            },
        ),
        migrations.CreateModel(
            name='SermonFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, default='', help_text="What does the file do? e.g. 'Sermon Outline', 'PowerPoint', 'Bible Study' etc...")),
                ('file', mezzanine.core.fields.FileField(max_length=255, help_text='Use the media manager to upload and select the', blank=True)),
                ('sermon', models.ForeignKey(to='mezzanine_sermons.Sermon')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SermonSeries',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=60, help_text='The name of the sermon series')),
                ('bible_passage', models.CharField(max_length=100, help_text='The bible passage for the sermon series', blank=True)),
                ('description', models.TextField()),
                ('start_date', models.DateField(help_text='This helps us order the sermon series')),
                ('image', mezzanine.core.fields.FileField(max_length=255, verbose_name='Image', help_text='Use the media manager to upload and select an image for the sermon series', blank=True)),
            ],
            options={
                'verbose_name': 'Sermon Series',
                'verbose_name_plural': 'Sermon Series',
            },
        ),
        migrations.AddField(
            model_name='sermon',
            name='series',
            field=models.ForeignKey(blank=True, to='mezzanine_sermons.SermonSeries', null=True),
        ),
    ]
