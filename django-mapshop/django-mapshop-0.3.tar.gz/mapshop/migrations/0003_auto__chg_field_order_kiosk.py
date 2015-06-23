# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Order.kiosk'
        db.alter_column(u'mapshop_order', 'kiosk_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Kiosk'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Order.kiosk'
        raise RuntimeError("Cannot reverse this migration. 'Order.kiosk' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Order.kiosk'
        db.alter_column(u'mapshop_order', 'kiosk_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Kiosk']))

    models = {
        u'mapshop.client': {
            'Meta': {'object_name': 'Client'},
            'account_org': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'add_phone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'address_org': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'bank_org': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bik_org': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'cor_account_org': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn_org': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'kpp_org': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_org': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notice_email': ('django.db.models.fields.BooleanField', [], {}),
            'notice_phone': ('django.db.models.fields.BooleanField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'postal_index_org': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'treatment': ('django.db.models.fields.CharField', [], {'default': "u'\\u0423\\u0432\\u0430\\u0436\\u0430\\u0435\\u043c\\u044b\\u0439'", 'max_length': '10'})
        },
        u'mapshop.kiosk': {
            'Meta': {'object_name': 'Kiosk'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'mapshop.order': {
            'Meta': {'object_name': 'Order'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Client']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kiosk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Kiosk']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'\\u041d\\u043e\\u0432\\u044b\\u0439'", 'max_length': '10'})
        },
        u'mapshop.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Product']"})
        },
        u'mapshop.preorder': {
            'Meta': {'object_name': 'Preorder'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Product']"})
        },
        u'mapshop.product': {
            'Meta': {'object_name': 'Product'},
            'available': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        u'mapshop.productimages': {
            'Meta': {'object_name': 'ProductImages'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Product']"})
        }
    }

    complete_apps = ['mapshop']