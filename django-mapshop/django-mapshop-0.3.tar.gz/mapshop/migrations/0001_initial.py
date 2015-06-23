# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Kiosk'
        db.create_table(u'mapshop_kiosk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('mnemonic', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'mapshop', ['Kiosk'])

        # Adding model 'Product'
        db.create_table(u'mapshop_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('available', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'mapshop', ['Product'])

        # Adding model 'ProductImages'
        db.create_table(u'mapshop_productimages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Product'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'mapshop', ['ProductImages'])

        # Adding model 'Client'
        db.create_table(u'mapshop_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('notice_email', self.gf('django.db.models.fields.BooleanField')()),
            ('notice_phone', self.gf('django.db.models.fields.BooleanField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'mapshop', ['Client'])

        # Adding model 'Order'
        db.create_table(u'mapshop_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'\u041d\u043e\u0432\u044b\u0439', max_length=10)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Client'])),
            ('kiosk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Kiosk'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'mapshop', ['Order'])

        # Adding model 'OrderItem'
        db.create_table(u'mapshop_orderitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Product'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'mapshop', ['OrderItem'])


    def backwards(self, orm):
        # Deleting model 'Kiosk'
        db.delete_table(u'mapshop_kiosk')

        # Deleting model 'Product'
        db.delete_table(u'mapshop_product')

        # Deleting model 'ProductImages'
        db.delete_table(u'mapshop_productimages')

        # Deleting model 'Client'
        db.delete_table(u'mapshop_client')

        # Deleting model 'Order'
        db.delete_table(u'mapshop_order')

        # Deleting model 'OrderItem'
        db.delete_table(u'mapshop_orderitem')


    models = {
        u'mapshop.client': {
            'Meta': {'object_name': 'Client'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice_email': ('django.db.models.fields.BooleanField', [], {}),
            'notice_phone': ('django.db.models.fields.BooleanField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11'})
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
            'kiosk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Kiosk']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'\\u041d\\u043e\\u0432\\u044b\\u0439'", 'max_length': '10'})
        },
        u'mapshop.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapshop.Order']"}),
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