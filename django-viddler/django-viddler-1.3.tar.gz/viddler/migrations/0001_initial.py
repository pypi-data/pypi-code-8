# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import durationfield.db.models.fields.duration
import queued_storage.backends
import django.core.validators
import dirtyfields.dirtyfields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ViddlerVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('viddler_id', models.CharField(help_text=b'The ID assigned by Viddler. Not editable.', verbose_name='Viddler ID', max_length=50, editable=False)),
                ('last_synced', models.DateTimeField(verbose_name='Last Synced', null=True, editable=False, blank=True)),
                ('status', models.CharField(verbose_name='Status', max_length=50, editable=False)),
                ('author', models.CharField(verbose_name='Author', max_length=50, editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('length', durationfield.db.models.fields.duration.DurationField(verbose_name='Length', editable=False)),
                ('description', models.TextField(verbose_name='Description')),
                ('age_limit', models.IntegerField(blank=True, help_text=b'A value between 9 and 99 or empty to reset', null=True, verbose_name='Age Limit', validators=[django.core.validators.MinValueValidator(9), django.core.validators.MaxValueValidator(99)])),
                ('url', models.URLField(help_text=b"Viddler's video URL", verbose_name='URL', editable=False)),
                ('embed_code', models.TextField(verbose_name='Embed Code', null=True, editable=False, blank=True)),
                ('thumbnail_url', models.URLField(help_text=b'The URL of the thumbnail', verbose_name='Thumbnail URL', editable=False)),
                ('key_image_custom', models.ImageField(upload_to=b'viddler/keyimage', width_field=b'key_image_custom_width', storage=queued_storage.backends.QueuedOverwriteFileStorage(), height_field=b'key_image_custom_height', blank=True, null=True, verbose_name='Key Image')),
                ('key_image_custom_width', models.IntegerField(null=True, blank=True)),
                ('key_image_custom_height', models.IntegerField(null=True, blank=True)),
                ('thumbnail', models.ImageField(upload_to=b'viddler/thumbnail', width_field=b'thumb_width', storage=queued_storage.backends.QueuedOverwriteFileStorage(), height_field=b'thumb_height', blank=True, editable=False, null=True)),
                ('thumb_width', models.IntegerField(null=True, editable=False, blank=True)),
                ('thumb_height', models.IntegerField(null=True, editable=False, blank=True)),
                ('permalink', models.URLField(help_text=b'The permanent link URL', verbose_name='Permalink')),
                ('html5_video_source', models.URLField(verbose_name='HTML5 Source URL', editable=False)),
                ('audio_only', models.BooleanField(default=False, verbose_name='Audio Only', editable=False)),
                ('view_count', models.IntegerField(verbose_name='View Count', editable=False)),
                ('impression_count', models.IntegerField(verbose_name='Impression Count', editable=False)),
                ('upload_time', models.DateTimeField(verbose_name='Upload Time', editable=False)),
                ('made_public_time', models.DateTimeField(verbose_name='Made Public Time', null=True, editable=False, blank=True)),
                ('favorite', models.IntegerField(verbose_name='Favorite', editable=False)),
                ('comment_count', models.IntegerField(verbose_name='Comment Count', editable=False)),
                ('tags', models.CharField(max_length=255, verbose_name='Tags', blank=True)),
                ('thumbnails_count', models.IntegerField(verbose_name='Thumbnails Count', editable=False)),
                ('thumbnail_index', models.IntegerField(verbose_name='Thumbnail Index', editable=False)),
                ('view_permission', models.CharField(max_length=50, verbose_name='View Permission', choices=[(b'private', b'Private (Only Me)'), (b'invite', b'Invitation Only (Anyone with an invitation)'), (b'embed', b'Domain Restricted (Anyone on allowed domains)'), (b'public', b'Public (Everyone)')])),
                ('embed_permission', models.CharField(max_length=50, verbose_name='Embed Permission', choices=[(b'private', b'Private (Only Me)'), (b'invite', b'Invitation Only (Anyone with an invitation)'), (b'embed', b'Domain Restricted (Anyone on allowed domains)'), (b'public', b'Public (Everyone)')])),
                ('tagging_permission', models.CharField(max_length=50, verbose_name='Tagging Permission', choices=[(b'private', b'Private (Only Me)'), (b'invite', b'Invitation Only (Anyone with an invitation)'), (b'embed', b'Domain Restricted (Anyone on allowed domains)'), (b'public', b'Public (Everyone)')])),
                ('commenting_permission', models.CharField(max_length=50, verbose_name='Commenting Permission', choices=[(b'private', b'Private (Only Me)'), (b'invite', b'Invitation Only (Anyone with an invitation)'), (b'embed', b'Domain Restricted (Anyone on allowed domains)'), (b'public', b'Public (Everyone)')])),
                ('download_permission', models.CharField(max_length=50, verbose_name='Download Permission', choices=[(b'private', b'Private (Only Me)'), (b'invite', b'Invitation Only (Anyone with an invitation)'), (b'embed', b'Domain Restricted (Anyone on allowed domains)'), (b'public', b'Public (Everyone)')])),
                ('display_aspect_ratio', models.CharField(verbose_name='Aspect Ratio', max_length=10, editable=False)),
                ('files', models.TextField(verbose_name='Files', editable=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Viddler Video',
                'verbose_name_plural': 'Viddler Videos',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
