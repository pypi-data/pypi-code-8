# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import textplusstuff.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StacksTextBlock',
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
                        help_text='The name of this Text Block.',
                        max_length=100,
                        verbose_name='Name'
                    )
                ),
                (
                    'content',
                    textplusstuff.fields.TextPlusStuffField(
                        help_text='Enter the content of your Text Block here.',
                        verbose_name='Content'
                    )
                ),
            ],
            options={
                'verbose_name': 'Text Block',
                'verbose_name_plural': 'Text Blocks',
            },
            bases=(models.Model,),
        ),
    ]
