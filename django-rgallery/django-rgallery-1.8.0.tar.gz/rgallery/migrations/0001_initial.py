# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('password', models.CharField(default=b'', max_length=255, null=True, verbose_name='Password', blank=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Folder',
                'verbose_name_plural': 'Folders',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('image', models.ImageField(upload_to=b'uploads/photos/', verbose_name='Image', blank=True)),
                ('video', models.FileField(upload_to=b'uploads/videos/', null=True, verbose_name='Video', blank=True)),
                ('origen', models.CharField(max_length=255, verbose_name='Source file')),
                ('insert_date', models.DateTimeField(verbose_name='Insert date')),
                ('capture_date', models.DateTimeField(verbose_name='Photo date')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('folder', models.ForeignKey(related_name='photo', verbose_name='Folder', blank=True, to='rgallery.Folder', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
    ]
