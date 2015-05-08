# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'assetcloud_userprofile')


    def backwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'assetcloud_userprofile', (
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profiles', to=orm['assetcloud.Account'])),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('original_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_registered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accepted_terms_and_conditions', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('accepted_aup', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('assetcloud', ['UserProfile'])


    models = {
        u'assetcloud.account': {
            'Meta': {'object_name': 'Account'},
            'header_background': ('assetcloud.models.ColourField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            'header_links': ('assetcloud.models.ColourField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            'header_links_active': ('assetcloud.models.ColourField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'organisation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['assetcloud.OrganisationType']", 'null': 'True', 'blank': 'True'}),
            'storage': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'storage_limit_override': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subdomain': ('assetcloud.models.NullableCharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'welcome_text': ('django.db.models.fields.TextField', [], {'default': "'Welcome to Asset Share, a tool for sharing and managing your digital assets.'", 'blank': 'True'})
        },
        u'assetcloud.accountcancellation': {
            'Meta': {'object_name': 'AccountCancellation'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cancellations'", 'to': u"orm['assetcloud.Account']"}),
            'better_product': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'budget': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'doesnt_have_features': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dont_use_it_enough': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra_detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'found_something_better': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'missing_features': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'should_keep_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'too_expensive': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'assetcloud.asset': {
            'Meta': {'object_name': 'Asset'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'__assets'", 'to': u"orm['assetcloud.Account']"}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('assetcloud.models.QuotaValidatingFileField', [], {'max_length': '2048', 'size_field_name': "'file_size'"}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assets'", 'to': u"orm['assetcloud.Upload']"})
        },
        u'assetcloud.assetimageinfo': {
            'Meta': {'object_name': 'AssetImageInfo'},
            'asset': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'_image_info'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['assetcloud.Asset']"}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        u'assetcloud.folder': {
            'Meta': {'object_name': 'Folder'},
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'folders'", 'symmetrical': 'False', 'to': u"orm['assetcloud.Asset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folders'", 'to': u"orm['auth.User']"})
        },
        u'assetcloud.indexstate': {
            'Meta': {'object_name': 'IndexState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'assetcloud.organisationtype': {
            'Meta': {'object_name': 'OrganisationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'assetcloud.share': {
            'Meta': {'object_name': 'Share'},
            'expiry': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'assetcloud.sharedasset': {
            'Meta': {'object_name': 'SharedAsset'},
            'asset_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'share': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shared_assets'", 'to': u"orm['assetcloud.Share']"})
        },
        u'assetcloud.upload': {
            'Meta': {'object_name': 'Upload'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['assetcloud']