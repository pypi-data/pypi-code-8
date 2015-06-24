# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('login_required', models.BooleanField(default=False)),
                ('plugin', models.CharField(blank=True, max_length=100, null=True)),
                ('weight', models.SmallIntegerField(default=0)),
                ('parameters', jsonfield.fields.JSONField(blank=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, related_name='children', to='navigation.Menu')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('path', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=100)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(editable=False, null=True, related_name='translations', to='navigation.Menu')),
            ],
            options={
                'db_table': 'navigation_menu_translation',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='menutranslation',
            unique_together=set([('language_code', 'master'), ('path', 'language_code')]),
        ),
    ]
