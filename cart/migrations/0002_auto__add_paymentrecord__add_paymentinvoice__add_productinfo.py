# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PayMentRecord'
        db.create_table(u'cart_paymentrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='record_product', to=orm['cart.ProductInfo'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_payment_record', to=orm['account.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('invoice', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='payment_record_invoice', unique=True, null=True, to=orm['cart.PayMentInvoice'])),
        ))
        db.send_create_signal(u'cart', ['PayMentRecord'])

        # Adding model 'PayMentInvoice'
        db.create_table(u'cart_paymentinvoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relate_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('print_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('donation', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('love_code', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('carruer_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('carruer_num', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('tax_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('inv_type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('invoice_rtn_msg', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('random_number', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('invalid_reason', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('invalid_rtn_code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('invalid_rtn_msg', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('invalid_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'cart', ['PayMentInvoice'])

        # Adding model 'ProductInfo'
        db.create_table(u'cart_productinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('trade_desc', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('item_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'cart', ['ProductInfo'])


    def backwards(self, orm):
        # Deleting model 'PayMentRecord'
        db.delete_table(u'cart_paymentrecord')

        # Deleting model 'PayMentInvoice'
        db.delete_table(u'cart_paymentinvoice')

        # Deleting model 'ProductInfo'
        db.delete_table(u'cart_productinfo')


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
        u'cart.cart': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Cart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cart.item': {
            'Meta': {'ordering': "('cart',)", 'object_name': 'Item'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cart.Cart']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'})
        },
        u'cart.paymentinvoice': {
            'Meta': {'object_name': 'PayMentInvoice'},
            'carruer_num': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'carruer_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'donation': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inv_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'invalid_reason': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'invalid_rtn_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'invalid_rtn_msg': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'invalid_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'invoice_rtn_msg': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'love_code': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'print_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'random_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'relate_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'tax_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        u'cart.paymentrecord': {
            'Meta': {'object_name': 'PayMentRecord'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'payment_record_invoice'", 'unique': 'True', 'null': 'True', 'to': u"orm['cart.PayMentInvoice']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'record_product'", 'to': u"orm['cart.ProductInfo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_payment_record'", 'to': u"orm['account.User']"})
        },
        u'cart.productinfo': {
            'Meta': {'object_name': 'ProductInfo'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'total_amount': ('django.db.models.fields.IntegerField', [], {}),
            'trade_desc': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cart']