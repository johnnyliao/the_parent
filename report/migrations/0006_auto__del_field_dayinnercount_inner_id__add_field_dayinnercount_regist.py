# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DayInnerCount.inner_id'
        db.delete_column(u'report_dayinnercount', 'inner_id')

        # Adding field 'DayInnerCount.register'
        db.add_column(u'report_dayinnercount', 'register',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='dayinnercounts', to=orm['report.Register']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'DayInnerCount.inner_id'
        db.add_column(u'report_dayinnercount', 'inner_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)

        # Deleting field 'DayInnerCount.register'
        db.delete_column(u'report_dayinnercount', 'register_id')


    models = {
        u'report.dayinnercount': {
            'Meta': {'object_name': 'DayInnerCount'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hit_count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dayinnercounts'", 'to': u"orm['report.Register']"})
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