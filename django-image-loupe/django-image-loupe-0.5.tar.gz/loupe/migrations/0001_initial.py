# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loupe.storage
import loupe.fields
import loupe.models
import dirtyfields.dirtyfields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoupeImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.CharField(max_length=255, verbose_name='slug')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('image', loupe.fields.LargeImageField(storage=loupe.storage.FileSystemTilesetStorage(), upload_to=loupe.models.slug_upload_to, blank=True, help_text='We will create an host the tileset form this image.', null=True, verbose_name='image')),
                ('external_tileset_url', models.URLField(help_text='The tileset for this image is hosted elsewhere.', null=True, verbose_name='external tileset URL', blank=True)),
                ('external_tileset_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='external tileset type', choices=[(b'dzi', b'Deep Zoom (DZI)'), (b'iif', b'International Image Interchage Format (IIF)'), (b'lip', b'Legacy Image Pyramid'), (b'osm', b'Open Street Maps (OSM)'), (b'tms', b'Tiled Map Service (TMS)'), (b'zoomify', b'Zoomify')])),
                ('image_height', models.IntegerField(verbose_name='image height', null=True, editable=False, blank=True)),
                ('image_width', models.IntegerField(verbose_name='image width', null=True, editable=False, blank=True)),
                ('tile_size', models.IntegerField(default=256, verbose_name='tile site', null=True, editable=False, blank=True)),
                ('base_tile_url', models.CharField(verbose_name='base tile URL', max_length=255, null=True, editable=False, blank=True)),
                ('thumbnail', models.FileField(upload_to=b'loupe_thumbs', null=True, verbose_name='thumbnail', blank=True)),
                ('document_name', models.CharField(help_text='If this image is part of a document, enter its name here. Make sure all parts of this document have the same "document name".', max_length=255, null=True, verbose_name='document name', blank=True)),
                ('document_order', models.IntegerField(help_text='The order in which this image appears in the document.', null=True, verbose_name='document order', blank=True)),
            ],
            options={
                'verbose_name': 'Loupe Image',
                'verbose_name_plural': 'Loupe Images',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
