# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('is_page', models.BooleanField(default=True)),
                ('created', models.DateTimeField(verbose_name='created', auto_now_add=True)),
                ('published', models.DateTimeField(blank=True, null=True, verbose_name='published')),
                ('allow_comments', models.BooleanField(verbose_name='allow comments', default=False)),
                ('template_name', models.CharField(blank=True, max_length=70, verbose_name='template name', help_text="Example: 'content/contact_page.html'. If this isn't provided, the system will use 'content/default.html'.")),
                ('registration_required', models.BooleanField(verbose_name='registration required', default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('text', models.TextField(blank=True, verbose_name='content')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(editable=False, null=True, related_name='translations', to='content.Content')),
            ],
            options={
                'db_table': 'content_content_translation',
                'permissions': (('Can list all content', 'list_contents'),),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='contenttranslation',
            unique_together=set([('language_code', 'master'), ('url', 'language_code')]),
        ),
    ]
