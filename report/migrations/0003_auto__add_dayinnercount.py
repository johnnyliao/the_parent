# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DayInnerCount'
        db.create_table(u'report_dayinnercount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('inner_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('hit_count', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('group', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'report', ['DayInnerCount'])


    def backwards(self, orm):
        # Deleting model 'DayInnerCount'
        db.delete_table(u'report_dayinnercount')


    models = {
        u'report.dayinnercount': {
            'Meta': {'object_name': 'DayInnerCount'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hit_count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
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