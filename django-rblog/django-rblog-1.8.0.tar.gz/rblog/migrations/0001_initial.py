# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rgallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_id', models.CharField(max_length=32, verbose_name='Comment id')),
                ('thread_id', models.CharField(max_length=32, verbose_name='Thread id')),
                ('thread_link', models.CharField(max_length=200, verbose_name='Thread link')),
                ('forum_id', models.CharField(max_length=32, verbose_name='Forum id')),
                ('body', models.TextField(verbose_name='Comment')),
                ('author_name', models.CharField(max_length=200, verbose_name='Author name')),
                ('author_email', models.CharField(max_length=200, verbose_name='Author email')),
                ('author_url', models.CharField(max_length=200, verbose_name='Author url')),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('text', models.TextField(verbose_name='Text')),
                ('image', models.ImageField(upload_to=b'images/posts', verbose_name='Image', blank=True)),
                ('hits', models.IntegerField(default=1, verbose_name='Hits', blank=True)),
                ('creation_date', models.DateTimeField(verbose_name='Creation date')),
                ('highlighted', models.BooleanField(default=False, verbose_name='Highlighted')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('thread_id', models.CharField(max_length=32, verbose_name='Disqus thread id', blank=True)),
                ('lang', models.CharField(blank=True, max_length=32, null=True, verbose_name='Language of the post', choices=[(b'es', b'Spanish'), (b'en', b'English')])),
                ('ptype', models.CharField(default=b'post', choices=[(b'post', b'Post'), (b'link', b'Link'), (b'photo', b'Photo'), (b'track', b'Track')], max_length=50, blank=True, null=True, verbose_name='Post type')),
                ('canonical', models.CharField(max_length=255, null=True, verbose_name='Canonical', blank=True)),
                ('robots', models.CharField(blank=True, max_length=50, null=True, verbose_name='Robots behavior', choices=[(b'index,follow', b'Index Follow'), (b'index,nofollow', b'Index NOfollow'), (b'noindex,follow', b'NOindex, Follow'), (b'noindex,nofollow', b'NOindex, NOfollow')])),
                ('redirect', models.URLField(help_text='Redirect the post to this url', max_length=255, null=True, verbose_name='Redirect', blank=True)),
                ('photo', models.ManyToManyField(related_name='photo', null=True, to='rgallery.Photo', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(related_name='post_from', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=(models.Model,),
        ),
    ]
