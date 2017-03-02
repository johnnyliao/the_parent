# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Register.web_type'
        db.add_column(u'report_register', 'web_type',
                      self.gf('django.db.models.fields.CharField')(default='ttshow', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Register.web_type'
        db.delete_column(u'report_register', 'web_type')


    models = {
        u'report.dayinnercount': {
            'Meta': {'object_name': 'DayInnerCount'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hit_count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'every_day_data'", 'to': u"orm['report.Register']"})
        },
        u'report.register': {
            'Meta': {'object_name': 'Register'},
            'base_count': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'web_type': ('django.db.models.fields.CharField', [], {'default': "'ttshow'", 'max_length': '20'})
        }
    }

    complete_apps = ['report']