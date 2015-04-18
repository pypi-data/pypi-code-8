# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServableContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServableHttpHeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileSource',
            fields=[
                ('source_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='localsrv.Source')),
                ('file_path', models.FileField(null=True, upload_to=b'')),
            ],
            bases=('localsrv.source',),
        ),
        migrations.CreateModel(
            name='StringSource',
            fields=[
                ('source_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='localsrv.Source')),
                ('string', models.TextField(max_length=20971520)),
            ],
            bases=('localsrv.source',),
        ),
        migrations.CreateModel(
            name='URLSource',
            fields=[
                ('source_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='localsrv.Source')),
                ('url', models.URLField()),
            ],
            bases=('localsrv.source',),
        ),
        migrations.AddField(
            model_name='servablecontent',
            name='headers',
            field=models.ManyToManyField(to='localsrv.ServableHttpHeader', blank=True),
        ),
        migrations.AddField(
            model_name='servablecontent',
            name='source',
            field=models.ForeignKey(to='localsrv.Source', null=True),
        ),
    ]
