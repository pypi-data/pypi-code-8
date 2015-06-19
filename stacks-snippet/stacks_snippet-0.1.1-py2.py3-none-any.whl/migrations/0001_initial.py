# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='The name of this HTML snippet. For internal use only.', max_length=100, verbose_name='Name')),
                ('snippet', models.TextField(help_text='The snippet of HTML.', verbose_name='HTML Snippet')),
            ],
        ),
    ]
