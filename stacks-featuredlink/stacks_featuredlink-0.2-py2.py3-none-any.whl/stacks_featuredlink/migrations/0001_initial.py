# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import textplusstuff.fields
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StacksFeaturedLink',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                (
                    'name',
                    models.CharField(
                        help_text='The name of this image.',
                        max_length=100,
                        verbose_name='Name'
                    )
                ),
                ('url', models.URLField(max_length=300, verbose_name='Name')),
                (
                    'image',
                    versatileimagefield.fields.VersatileImageField(
                        upload_to=b'stacks_featuredlink/',
                        blank=True
                    )
                ),
                (
                    'image_ppoi',
                    versatileimagefield.fields.PPOIField(
                        default='0.5x0.5',
                        max_length=20,
                        editable=False
                    )
                ),
                (
                    'optional_content',
                    textplusstuff.fields.TextPlusStuffField(
                        help_text='A field to enter optional accompanying '
                                  'content.',
                        verbose_name='Optional Content',
                        blank=True
                    )
                ),
            ],
            options={
                'verbose_name': 'Stacks Featured Link',
                'verbose_name_plural': 'Stacks Featured Links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StacksFeaturedLinkList',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                (
                    'list_name',
                    models.CharField(
                        help_text='The name of this image list.',
                        max_length=100,
                        verbose_name='List Name'
                    )
                ),
            ],
            options={
                'verbose_name': 'Stacks Featured Link List',
                'verbose_name_plural': 'Stacks Featured Link List',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StacksFeaturedLinkListLink',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveIntegerField()),
                (
                    'link',
                    models.ForeignKey(
                        to='stacks_featuredlink.StacksFeaturedLink'
                    )
                ),
                (
                    'link_list',
                    models.ForeignKey(
                        to='stacks_featuredlink.StacksFeaturedLinkList'
                    )
                ),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stacksfeaturedlinklist',
            name='links',
            field=models.ManyToManyField(
                to='stacks_featuredlink.StacksFeaturedLink',
                through='stacks_featuredlink.StacksFeaturedLinkListLink'
            ),
            preserve_default=True,
        ),
    ]
