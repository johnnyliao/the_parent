# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DayInnerCount.date'
        db.alter_column(u'report_dayinnercount', 'date', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'DayInnerCount.date'
        db.alter_column(u'report_dayinnercount', 'date', self.gf('django.db.models.fields.DateField')(auto_now=True))

    models = {
        u'report.dayinnercount': {
            'Meta': {'object_name': 'DayInnerCount'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hit_count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'report.register': {
            'Meta': {'object_name': 'Register'},
            'base_count': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['report']