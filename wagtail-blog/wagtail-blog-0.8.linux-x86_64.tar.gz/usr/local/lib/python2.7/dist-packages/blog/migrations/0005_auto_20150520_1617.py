# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('blog', '0004_auto_20150427_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.tag',),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='blog_categories',
            field=models.ManyToManyField(to='blog.BlogCategory', blank=True, through='blog.BlogCategoryBlogPage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='parent',
            field=models.ForeignKey(to='blog.BlogCategory', blank=True, help_text='Categories, unlike tags, can have a hierarchy. You might have a Jazz category, and under that have children categories for Bebop and Big Band. Totally optional.', null=True, related_name='children'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(help_text='This date may be displayed on the blog post. It is not used to schedule posts to go live at a later date.', default=datetime.datetime.today, verbose_name='Post date'),
            preserve_default=True,
        ),
    ]
