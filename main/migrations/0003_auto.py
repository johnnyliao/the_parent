# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field brand on 'BrandIndex'
        m2m_table_name = db.shorten_name(u'main_brandindex_brand')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brandindex', models.ForeignKey(orm[u'main.brandindex'], null=False)),
            ('brand', models.ForeignKey(orm[u'cart.brand'], null=False))
        ))
        db.create_unique(m2m_table_name, ['brandindex_id', 'brand_id'])


    def backwards(self, orm):
        # Removing M2M table for field brand on 'BrandIndex'
        db.delete_table(db.shorten_name(u'main_brandindex_brand'))


    models = {
        u'cart.brand': {
            'Meta': {'object_name': 'Brand'},
            'banner': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brand_banner'", 'symmetrical': 'False', 'to': u"orm['cart.BrandBanner']"}),
            'brand_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'movie': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brand_movie'", 'symmetrical': 'False', 'to': u"orm['cart.BrandMovie']"})
        },
        u'cart.brandbanner': {
            'Meta': {'object_name': 'BrandBanner'},
            'banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'cart.brandmovie': {
            'Meta': {'object_name': 'BrandMovie'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'main.brandindex': {
            'Meta': {'object_name': 'BrandIndex'},
            'banner': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brand_index_banner'", 'symmetrical': 'False', 'to': u"orm['main.BrandIndexBanner']"}),
            'brand': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'index_brands'", 'symmetrical': 'False', 'to': u"orm['cart.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brand_index_movie'", 'symmetrical': 'False', 'to': u"orm['main.BrandIndexMovie']"})
        },
        u'main.brandindexbanner': {
            'Meta': {'object_name': 'BrandIndexBanner'},
            'banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'main.brandindexmovie': {
            'Meta': {'object_name': 'BrandIndexMovie'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'main.s3data': {
            'Meta': {'object_name': 'S3Data'},
            'bucket': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['main']