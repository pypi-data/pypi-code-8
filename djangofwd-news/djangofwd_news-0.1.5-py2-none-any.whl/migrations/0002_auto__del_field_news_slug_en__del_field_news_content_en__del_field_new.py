# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'News.slug_en'
        db.delete_column(u'news_news', 'slug_en')

        # Deleting field 'News.content_en'
        db.delete_column(u'news_news', 'content_en')

        # Deleting field 'News.summary_en'
        db.delete_column(u'news_news', 'summary_en')

        # Deleting field 'News.title_en'
        db.delete_column(u'news_news', 'title_en')

        # Deleting field 'Category.slug_en'
        db.delete_column(u'news_category', 'slug_en')

        # Deleting field 'Category.name_en'
        db.delete_column(u'news_category', 'name_en')

        # Deleting field 'Attachment.slug_en'
        db.delete_column(u'news_attachment', 'slug_en')

        # Deleting field 'Attachment.name_en'
        db.delete_column(u'news_attachment', 'name_en')

        # Deleting field 'Gallery.slug_en'
        db.delete_column(u'news_gallery', 'slug_en')

        # Deleting field 'Gallery.title_en'
        db.delete_column(u'news_gallery', 'title_en')

        # Deleting field 'Tag.slug_en'
        db.delete_column(u'news_tag', 'slug_en')

        # Deleting field 'Tag.name_en'
        db.delete_column(u'news_tag', 'name_en')


    def backwards(self, orm):
        # Adding field 'News.slug_en'
        db.add_column(u'news_news', 'slug_en',
                      self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'News.content_en'
        db.add_column(u'news_news', 'content_en',
                      self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'News.summary_en'
        db.add_column(u'news_news', 'summary_en',
                      self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'News.title_en'
        db.add_column(u'news_news', 'title_en',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.slug_en'
        db.add_column(u'news_category', 'slug_en',
                      self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_en'
        db.add_column(u'news_category', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Attachment.slug_en'
        db.add_column(u'news_attachment', 'slug_en',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Attachment.name_en'
        db.add_column(u'news_attachment', 'name_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Gallery.slug_en'
        db.add_column(u'news_gallery', 'slug_en',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Gallery.title_en'
        db.add_column(u'news_gallery', 'title_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Tag.slug_en'
        db.add_column(u'news_tag', 'slug_en',
                      self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Tag.name_en'
        db.add_column(u'news_tag', 'name_en',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True),
                      keep_default=False)


    models = {
        u'news.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'news_attachments'", 'null': 'True', 'blank': 'True', 'to': u"orm['news.News']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'news.author': {
            'Meta': {'object_name': 'Author'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'news.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'news.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'news_gallery'", 'null': 'True', 'blank': 'True', 'to': u"orm['news.News']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'news.news': {
            'Meta': {'object_name': 'News'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'authors'", 'null': 'True', 'to': u"orm['news.Author']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'news_category'", 'to': u"orm['news.Category']"}),
            'content': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'summary': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'news_tags'", 'default': 'None', 'to': u"orm['news.Tag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'news.tag': {
            'Meta': {'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['news']