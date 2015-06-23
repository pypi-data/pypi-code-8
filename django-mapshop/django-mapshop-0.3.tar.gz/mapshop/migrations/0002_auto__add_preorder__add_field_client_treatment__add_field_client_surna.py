# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from decimal import Decimal
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Preorder'
        db.create_table(u'mapshop_preorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Product'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapshop.Client'])),
        ))
        db.send_create_signal(u'mapshop', ['Preorder'])

        # Adding field 'Client.treatment'
        db.add_column(u'mapshop_client', 'treatment',
                      self.gf('django.db.models.fields.CharField')(default=u'\u0423\u0432\u0430\u0436\u0430\u0435\u043c\u044b\u0439', max_length=10),
                      keep_default=False)

        # Adding field 'Client.surname'
        db.add_column(u'mapshop_client', 'surname',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.name'
        db.add_column(u'mapshop_client', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.add_phone'
        db.add_column(u'mapshop_client', 'add_phone',
                      self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.birthday'
        db.add_column(u'mapshop_client', 'birthday',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 6, 2, 0, 0)),
                      keep_default=False)

        # Adding field 'Client.is_organization'
        db.add_column(u'mapshop_client', 'is_organization',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Client.name_org'
        db.add_column(u'mapshop_client', 'name_org',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2015, 6, 2, 0, 0), max_length=100),
                      keep_default=False)

        # Adding field 'Client.address_org'
        db.add_column(u'mapshop_client', 'address_org',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2015, 6, 2, 0, 0), max_length=200),
                      keep_default=False)

        # Adding field 'Client.postal_index_org'
        db.add_column(u'mapshop_client', 'postal_index_org',
                      self.gf('django.db.models.fields.DecimalField')(default=Decimal('0.00'), max_digits=5, decimal_places=2),
                      keep_default=False)

        # Adding field 'Client.inn_org'
        db.add_column(u'mapshop_client', 'inn_org',
                      self.gf('django.db.models.fields.DecimalField')(default=Decimal('0.00'), max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Client.kpp_org'
        db.add_column(u'mapshop_client', 'kpp_org',
                      self.gf('django.db.models.fields.DecimalField')(default=Decimal('0.00'), max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Client.account_org'
        db.add_column(u'mapshop_client', 'account_org',
                      self.gf('django.db.models.fields.DecimalField')(default=Decimal('0.00'), max_digits=16, decimal_places=2),
                      keep_default=False)

        # Adding field 'Client.bank_org'
        db.add_column(u'mapshop_client', 'bank_org',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2015, 6, 2, 0, 0), max_length=100),
                      keep_default=False)

        # Adding field 'Client.cor_account_org'
        db.add_column(u'mapshop_client', 'cor_account_org',
                      self.gf('django.db.models.fields.DecimalField')(default=Decimal('0.00'), max_digits=16, decimal_places=2),
                      keep_default=False)

        # Adding field 'Client.bik_org'
        db.add_column(u'mapshop_client', 'bik_org',
                      self.gf('django.db.models.fields.DecimalField')(default=Decimal('0.00'), max_digits=9, decimal_places=2),
                      keep_default=False)


        # Changing field 'Client.phone'
        db.alter_column(u'mapshop_client', 'phone', self.gf('django.db.models.fields.CharField')(max_length=11, null=True))

    def backwards(self, orm):
        # Deleting model 'Preorder'
        db.delete_table(u'mapshop_preorder')

        # Deleting field 'Client.treatment'
        db.delete_column(u'mapshop_client', 'treatment')

        # Deleting field 'Client.surname'
        db.delete_column(u'mapshop_client', 'surname')

        # Deleting field 'Client.name'
        db.delete_column(u'mapshop_client', 'name')

        # Deleting field 'Client.add_phone'
        db.delete_column(u'mapshop_client', 'add_phone')

        # Deleting field 'Client.birthday'
        db.delete_column(u'mapshop_client', 'birthday')

        # Deleting field 'Client.is_organization'
        db.delete_column(u'mapshop_client', 'is_organization')

        # Deleting field 'Client.name_org'
        db.delete_column(u'mapshop_client', 'name_org')

        # Deleting field 'Client.address_org'
        db.delete_column(u'mapshop_client', 'address_org')

        # Deleting field 'Client.postal_index_org'
        db.delete_column(u'mapshop_client', 'postal_index_org')

        # Deleting field 'Client.inn_org'
        db.delete_column(u'mapshop_client', 'inn_org')

        # Deleting field 'Client.kpp_org'
        db.delete_column(u'mapshop_client', 'kpp_org')

        # Deleting field 'Client.account_org'
        db.delete_column(u'mapshop_client', 'account_org')

        # Deleting field 'Client.bank_org'
        db.delete_column(u'mapshop_client', 'bank_org')

        # Deleting field 'Client.cor_account_org'
        db.delete_column(u'mapshop_client', 'cor_account_org')

        # Deleting field 'Client.bik_org'
        db.delete_column(u'mapshop_client', 'bik_org')


        # Changing field 'Client.phone'
        db.alter_column(u'mapshop_client', 'phone', self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2015, 6, 2, 0, 0), max_length=11))

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