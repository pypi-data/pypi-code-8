# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_catalog', models.BooleanField(verbose_name='This page is a catalog')),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page')),
                ('public_extension', models.OneToOneField(related_name='draft_extension', null=True, editable=False, to='cmsplugin_catalog.CatalogExtension')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CatalogPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('panel_type', models.CharField(default=b'info', max_length=10, verbose_name='Bootstrap panel type', blank=True, choices=[(b'primary', b'primary'), (b'success', b'success'), (b'info', b'info'), (b'warning', b'warning'), (b'danger', b'danger')])),
                ('panel_header_link', models.BooleanField(verbose_name='Panel header link to catalog page')),
                ('panel_footer_text', models.CharField(max_length=500, null=True, verbose_name='Panel footer text', blank=True)),
                ('panel_footer_link', models.BooleanField(verbose_name='Panel footer link to catalog page')),
                ('panel_after_content', models.BooleanField(verbose_name='After the panel body has a placeholder')),
                ('display_panel_header', models.BooleanField(default=True, verbose_name='Display panel header')),
                ('display_level', models.CharField(default=b'currchild', max_length=50, verbose_name='Which level catalog to show', choices=[(b'child', 'Child catalog pages'), (b'current', 'Current catalog pages'), (b'currchild', 'Current and child catalog pages')])),
                ('line_length', models.PositiveSmallIntegerField(default=30, help_text='Zero mean unlimited.', verbose_name='Length of every line')),
                ('page_count', models.PositiveSmallIntegerField(default=5, verbose_name='How much page display')),
                ('display_date', models.BooleanField(verbose_name='Show page date in line')),
                ('catalog', models.ForeignKey(verbose_name='Catalog', to='cmsplugin_catalog.CatalogExtension', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
