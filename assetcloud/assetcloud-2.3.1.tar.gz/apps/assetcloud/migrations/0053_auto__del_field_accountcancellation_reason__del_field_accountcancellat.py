# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AccountCancellation.reason'
        db.delete_column('assetcloud_accountcancellation', 'reason')

        # Deleting field 'AccountCancellation.can_contact_when_addressed'
        db.delete_column('assetcloud_accountcancellation', 'can_contact_when_addressed')

        # Adding field 'AccountCancellation.too_expensive'
        db.add_column('assetcloud_accountcancellation', 'too_expensive',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AccountCancellation.budget'
        db.add_column('assetcloud_accountcancellation', 'budget',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'AccountCancellation.doesnt_have_features'
        db.add_column('assetcloud_accountcancellation', 'doesnt_have_features',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AccountCancellation.missing_features'
        db.add_column('assetcloud_accountcancellation', 'missing_features',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'AccountCancellation.found_something_better'
        db.add_column('assetcloud_accountcancellation', 'found_something_better',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AccountCancellation.better_product'
        db.add_column('assetcloud_accountcancellation', 'better_product',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'AccountCancellation.dont_use_it_enough'
        db.add_column('assetcloud_accountcancellation', 'dont_use_it_enough',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'AccountCancellation.reason'
        raise RuntimeError("Cannot reverse this migration. 'AccountCancellation.reason' and its values cannot be restored.")
        # Adding field 'AccountCancellation.can_contact_when_addressed'
        db.add_column('assetcloud_accountcancellation', 'can_contact_when_addressed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'AccountCancellation.too_expensive'
        db.delete_column('assetcloud_accountcancellation', 'too_expensive')

        # Deleting field 'AccountCancellation.budget'
        db.delete_column('assetcloud_accountcancellation', 'budget')

        # Deleting field 'AccountCancellation.doesnt_have_features'
        db.delete_column('assetcloud_accountcancellation', 'doesnt_have_features')

        # Deleting field 'AccountCancellation.missing_features'
        db.delete_column('assetcloud_accountcancellation', 'missing_features')

        # Deleting field 'AccountCancellation.found_something_better'
        db.delete_column('assetcloud_accountcancellation', 'found_something_better')

        # Deleting field 'AccountCancellation.better_product'
        db.delete_column('assetcloud_accountcancellation', 'better_product')

        # Deleting field 'AccountCancellation.dont_use_it_enough'
        db.delete_column('assetcloud_accountcancellation', 'dont_use_it_enough')


    models = {
        'assetcloud.account': {
            'Meta': {'object_name': 'Account'},
            'header_background': ('assetcloud.models.ColourField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            'header_links': ('assetcloud.models.ColourField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            'header_links_active': ('assetcloud.models.ColourField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'organisation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assetcloud.OrganisationType']", 'null': 'True', 'blank': 'True'}),
            'subdomain': ('assetcloud.models.NullableCharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'welcome_text': ('django.db.models.fields.TextField', [], {'default': "'Welcome to Asset Share, a tool for sharing and managing your digital assets.'", 'blank': 'True'})
        },
        'assetcloud.accountcancellation': {
            'Meta': {'object_name': 'AccountCancellation'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cancellations'", 'to': "orm['assetcloud.Account']"}),
            'better_product': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'budget': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'doesnt_have_features': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dont_use_it_enough': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra_detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'found_something_better': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'missing_features': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'should_keep_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'too_expensive': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'assetcloud.asset': {
            'Meta': {'object_name': 'Asset'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'__assets'", 'null': 'True', 'to': "orm['assetcloud.Account']"}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assets'", 'to': "orm['assetcloud.Upload']"})
        },
        'assetcloud.assetimageinfo': {
            'Meta': {'object_name': 'AssetImageInfo'},
            'asset': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'_image_info'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['assetcloud.Asset']"}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'assetcloud.folder': {
            'Meta': {'object_name': 'Folder'},
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'folders'", 'symmetrical': 'False', 'to': "orm['assetcloud.Asset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folders'", 'to': "orm['auth.User']"})
        },
        'assetcloud.indexstate': {
            'Meta': {'object_name': 'IndexState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'assetcloud.organisationtype': {
            'Meta': {'object_name': 'OrganisationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'assetcloud.share': {
            'Meta': {'object_name': 'Share'},
            'expiry': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'assetcloud.sharedasset': {
            'Meta': {'object_name': 'SharedAsset'},
            'asset_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'share': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shared_assets'", 'to': "orm['assetcloud.Share']"})
        },
        'assetcloud.upload': {
            'Meta': {'object_name': 'Upload'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'assetcloud.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profiles'", 'to': "orm['assetcloud.Account']"}),
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['assetcloud']