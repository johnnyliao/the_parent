# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ReportUser.supervisor'
        db.alter_column(u'report_reportuser', 'supervisor', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ReportUser.target'
        db.alter_column(u'report_reportuser', 'target', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'ReportUser.job_start'
        db.alter_column(u'report_reportuser', 'job_start', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'ReportUser.month_target'
        db.alter_column(u'report_reportuser', 'month_target', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'ReportUser.week_target'
        db.alter_column(u'report_reportuser', 'week_target', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'ReportUser.phone'
        db.alter_column(u'report_reportuser', 'phone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'ReportUser.fans_target'
        db.alter_column(u'report_reportuser', 'fans_target', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'ReportUser.kpi'
        db.alter_column(u'report_reportuser', 'kpi', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'ReportUser.email'
        db.alter_column(u'report_reportuser', 'email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True))

        # Changing field 'ReportUser.name'
        db.alter_column(u'report_reportuser', 'name', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

    def backwards(self, orm):

        # Changing field 'ReportUser.supervisor'
        db.alter_column(u'report_reportuser', 'supervisor', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'ReportUser.target'
        db.alter_column(u'report_reportuser', 'target', self.gf('django.db.models.fields.IntegerField')(default=''))

        # Changing field 'ReportUser.job_start'
        db.alter_column(u'report_reportuser', 'job_start', self.gf('django.db.models.fields.DateField')(default=''))

        # Changing field 'ReportUser.month_target'
        db.alter_column(u'report_reportuser', 'month_target', self.gf('django.db.models.fields.IntegerField')(default=''))

        # Changing field 'ReportUser.week_target'
        db.alter_column(u'report_reportuser', 'week_target', self.gf('django.db.models.fields.IntegerField')(default=''))

        # Changing field 'ReportUser.phone'
        db.alter_column(u'report_reportuser', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=10))

        # Changing field 'ReportUser.fans_target'
        db.alter_column(u'report_reportuser', 'fans_target', self.gf('django.db.models.fields.IntegerField')(default=''))

        # Changing field 'ReportUser.kpi'
        db.alter_column(u'report_reportuser', 'kpi', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'ReportUser.email'
        db.alter_column(u'report_reportuser', 'email', self.gf('django.db.models.fields.EmailField')(default='', max_length=254))

        # Changing field 'ReportUser.name'
        db.alter_column(u'report_reportuser', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=10))

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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'fans_target': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'kpi': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'month_target': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'week_target': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['report']