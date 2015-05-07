# -*- coding: utf-8 -*-
from PIL import Image
from django.conf import settings
from django.core.files.storage import DefaultStorage
from south.v2 import DataMigration
import importlib
import mimetypes
import os.path


def get_asset_storage():
    asset_storage_module = getattr(settings, 'ASSET_FILE_STORAGE', None)

    if asset_storage_module:
        mod_str, cls_str = asset_storage_module.rsplit('.', 1)
        asset_storage_class = getattr(importlib.import_module(mod_str), cls_str)
    else:
        asset_storage_class = DefaultStorage

    return asset_storage_class()


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        Asset = orm['assetcloud.Asset']
        # storage attribute of file fields is not included in the models
        # dict, so we have to set it here otherwise the default storage will
        # be used for everything, which will result in "no such file or
        # directory" errors when we try to migrate assets whose files are
        # stored in S3
        Asset._meta.get_field('file').storage = get_asset_storage()
        AssetImageInfo = orm['assetcloud.AssetImageInfo']
        for asset in Asset.objects.all():
            self.create_for_asset(asset, AssetImageInfo)

    def create_for_asset(self, asset, AssetImageInfo):
        if not self._is_unsupported_image_type(asset):
            mimetype, encoding = mimetypes.guess_type(asset.filename)
            if mimetype and mimetype.split('/')[0] == 'image':
                width, height = Image.open(asset.file).size
                aii = AssetImageInfo(asset=asset,
                                     height=height,
                                     width=width)
                aii.save()

    def _is_unsupported_image_type(self, asset):
        (filename, extension) = os.path.splitext(asset.filename)
        extension = extension.lower()

        image_extensions_not_supported_by_sorl = ['.tif', '.tiff', '.psd']

        if extension in image_extensions_not_supported_by_sorl:
            return True

        return False


    def backwards(self, orm):
        "Write your backwards methods here."
        orm['assetcloud.AssetImageInfo'].objects.all().delete()


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
            'welcome_text': ('django.db.models.fields.TextField', [], {'default': "'Welcome to Asset Cloud, a tool for sharing and managing your digital assets.'", 'blank': 'True'})
        },
        'assetcloud.asset': {
            'Meta': {'object_name': 'Asset'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'__assets'", 'null': 'True', 'to': "orm['assetcloud.Account']"}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'})
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
        'assetcloud.organisationtype': {
            'Meta': {'object_name': 'OrganisationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'assetcloud.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assetcloud.Account']"}),
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
    symmetrical = True
