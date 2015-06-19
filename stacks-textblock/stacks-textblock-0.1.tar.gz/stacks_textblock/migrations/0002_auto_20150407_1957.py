# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_textblock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StacksTextBlockList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('list_name', models.CharField(help_text='The name of this image list.', max_length=100, verbose_name='List Name')),
            ],
            options={
                'verbose_name': 'Stacks Text Block List',
                'verbose_name_plural': 'Stacks Text Block List',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StacksTextBlockListTextBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveIntegerField()),
                ('text_block', models.ForeignKey(to='stacks_textblock.StacksTextBlock')),
                ('text_block_list', models.ForeignKey(to='stacks_textblock.StacksTextBlockList')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stackstextblocklist',
            name='text_blocks',
            field=models.ManyToManyField(to='stacks_textblock.StacksTextBlock', through='stacks_textblock.StacksTextBlockListTextBlock'),
            preserve_default=True,
        ),
    ]
