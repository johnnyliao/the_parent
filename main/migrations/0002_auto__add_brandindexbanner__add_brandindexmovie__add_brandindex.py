# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BrandIndexBanner'
        db.create_table(u'main_brandindexbanner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('banner', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'main', ['BrandIndexBanner'])

        # Adding model 'BrandIndexMovie'
        db.create_table(u'main_brandindexmovie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'main', ['BrandIndexMovie'])

        # Adding model 'BrandIndex'
        db.create_table(u'main_brandindex', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'main', ['BrandIndex'])

        # Adding M2M table for field banner on 'BrandIndex'
        m2m_table_name = db.shorten_name(u'main_brandindex_banner')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brandindex', models.ForeignKey(orm[u'main.brandindex'], null=False)),
            ('brandindexbanner', models.ForeignKey(orm[u'main.brandindexbanner'], null=False))
        ))
        db.create_unique(m2m_table_name, ['brandindex_id', 'brandindexbanner_id'])

        # Adding M2M table for field movie on 'BrandIndex'
        m2m_table_name = db.shorten_name(u'main_brandindex_movie')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brandindex', models.ForeignKey(orm[u'main.brandindex'], null=False)),
            ('brandindexmovie', models.ForeignKey(orm[u'main.brandindexmovie'], null=False))
        ))
        db.create_unique(m2m_table_name, ['brandindex_id', 'brandindexmovie_id'])


    def backwards(self, orm):
        # Deleting model 'BrandIndexBanner'
        db.delete_table(u'main_brandindexbanner')

        # Deleting model 'BrandIndexMovie'
        db.delete_table(u'main_brandindexmovie')

        # Deleting model 'BrandIndex'
        db.delete_table(u'main_brandindex')

        # Removing M2M table for field banner on 'BrandIndex'
        db.delete_table(db.shorten_name(u'main_brandindex_banner'))

        # Removing M2M table for field movie on 'BrandIndex'
        db.delete_table(db.shorten_name(u'main_brandindex_movie'))


    models = {
        u'main.brandindex': {
            'Meta': {'object_name': 'BrandIndex'},
            'banner': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brand_index_banner'", 'symmetrical': 'False', 'to': u"orm['main.BrandIndexBanner']"}),
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