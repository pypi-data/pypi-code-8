# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CatalogPlugin'
        db.create_table(u'cmsplugin_catalog_catalogplugin', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('panel_type', self.gf('django.db.models.fields.CharField')(default='info', max_length=10, blank=True)),
            ('panel_header_link', self.gf('django.db.models.fields.BooleanField')()),
            ('panel_footer_text', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('panel_footer_link', self.gf('django.db.models.fields.BooleanField')()),
            ('panel_after_content', self.gf('django.db.models.fields.BooleanField')()),
            ('display_panel_header', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('display_level', self.gf('django.db.models.fields.CharField')(default='currchild', max_length=50)),
            ('line_length', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30)),
            ('page_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5)),
            ('display_date', self.gf('django.db.models.fields.BooleanField')()),
            ('catalog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsplugin_catalog.CatalogExtension'], null=True)),
        ))
        db.send_create_signal(u'cmsplugin_catalog', ['CatalogPlugin'])

        # Adding model 'CatalogExtension'
        db.create_table(u'cmsplugin_catalog_catalogextension', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public_extension', self.gf('django.db.models.fields.related.OneToOneField')(related_name='draft_extension', unique=True, null=True, to=orm['cmsplugin_catalog.CatalogExtension'])),
            ('extended_object', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.Page'], unique=True)),
            ('is_catalog', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'cmsplugin_catalog', ['CatalogExtension'])


    def backwards(self, orm):
        # Deleting model 'CatalogPlugin'
        db.delete_table(u'cmsplugin_catalog_catalogplugin')

        # Deleting model 'CatalogExtension'
        db.delete_table(u'cmsplugin_catalog_catalogextension')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.page': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('publisher_is_draft', 'application_namespace'), ('reverse_id', 'site', 'publisher_is_draft'))", 'object_name': 'Page'},
            'application_namespace': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'application_urls': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'changed_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_home': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'limit_visibility_in_menu': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'navigation_extenders': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cms.Page']"}),
            'placeholders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cms.Placeholder']", 'symmetrical': 'False'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.Page']"}),
            'reverse_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'revision_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'djangocms_pages'", 'to': u"orm['sites.Site']"}),
            'soft_root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'INHERIT'", 'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'xframe_options': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'cmsplugin_catalog.catalogextension': {
            'Meta': {'object_name': 'CatalogExtension'},
            'extended_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.Page']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_catalog': ('django.db.models.fields.BooleanField', [], {}),
            'public_extension': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'draft_extension'", 'unique': 'True', 'null': 'True', 'to': u"orm['cmsplugin_catalog.CatalogExtension']"})
        },
        u'cmsplugin_catalog.catalogplugin': {
            'Meta': {'object_name': 'CatalogPlugin', '_ormbases': ['cms.CMSPlugin']},
            'catalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsplugin_catalog.CatalogExtension']", 'null': 'True'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'display_date': ('django.db.models.fields.BooleanField', [], {}),
            'display_level': ('django.db.models.fields.CharField', [], {'default': "'currchild'", 'max_length': '50'}),
            'display_panel_header': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'line_length': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'page_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'panel_after_content': ('django.db.models.fields.BooleanField', [], {}),
            'panel_footer_link': ('django.db.models.fields.BooleanField', [], {}),
            'panel_footer_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'panel_header_link': ('django.db.models.fields.BooleanField', [], {}),
            'panel_type': ('django.db.models.fields.CharField', [], {'default': "'info'", 'max_length': '10', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cmsplugin_catalog']
