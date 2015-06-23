# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.available'
        db.delete_column(u'mapshop_product', 'available')

        # Adding field 'Product.ammount'
        db.add_column(u'mapshop_product', 'ammount',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Product.available'
        db.add_column(u'mapshop_product', 'available',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Product.ammount'
        db.delete_column(u'mapshop_product', 'ammount')


    models = {
        u'mapshop.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'mapshop.client': {
            'Meta': {'object_name': 'Client'},
            'account_org': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'add_phone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'address_org': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'bank_org': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bik_org': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cor_account_org': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn_org': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'kpp_org': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_org': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'notice_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notice_phone': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'postal_index_org': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'mapshop.kiosk': {
            'Meta': {'object_name': 'Kiosk'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scheduler': ('django.db.models.fields.CharField', [], {'default': "'\\xd1\\x81 9 \\xd0\\xb4\\xd0\\xbe 6 \\xd0\\xb2 \\xd0\\xb1\\xd1\\x83\\xd0\\xb4\\xd0\\xbd\\xd0\\xb8'", 'max_length': '200'})
        },
        u'mapshop.order': {
            'Meta': {'object_name': 'Order'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Client']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kiosk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Kiosk']", 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'\\u041d\\u043e\\u0432\\u044b\\u0439'", 'max_length': '10'})
        },
        u'mapshop.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'ammount': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Product']"})
        },
        u'mapshop.preorder': {
            'Meta': {'object_name': 'Preorder'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Client']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Product']"})
        },
        u'mapshop.product': {
            'Meta': {'object_name': 'Product'},
            'ammount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Category']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'mapshop.productimages': {
            'Meta': {'object_name': 'ProductImages'},
            'cropping': (u'django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Product']"})
        }
    }

    complete_apps = ['mapshop']