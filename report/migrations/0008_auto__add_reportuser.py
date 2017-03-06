# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReportUser'
        db.create_table(u'report_reportuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('job_start', self.gf('django.db.models.fields.DateField')()),
            ('target', self.gf('django.db.models.fields.IntegerField')()),
            ('week_target', self.gf('django.db.models.fields.IntegerField')()),
            ('month_target', self.gf('django.db.models.fields.IntegerField')()),
            ('fans_target', self.gf('django.db.models.fields.IntegerField')()),
            ('supervisor', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('kpi', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'report', ['ReportUser'])


    def backwards(self, orm):
        # Deleting model 'ReportUser'
        db.delete_table(u'report_reportuser')


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
        },
        u'report.reportuser': {
            'Meta': {'object_name': 'ReportUser'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'fans_target': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_start': ('django.db.models.fields.DateField', [], {}),
            'kpi': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'month_target': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'supervisor': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'target': ('django.db.models.fields.IntegerField', [], {}),
            'week_target': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['report']