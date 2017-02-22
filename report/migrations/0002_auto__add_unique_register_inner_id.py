# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Register', fields ['inner_id']
        db.create_unique(u'report_register', ['inner_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Register', fields ['inner_id']
        db.delete_unique(u'report_register', ['inner_id'])


    models = {
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