# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'S3Data'
        db.create_table(u'main_s3data', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('bucket', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'main', ['S3Data'])


    def backwards(self, orm):
        # Deleting model 'S3Data'
        db.delete_table(u'main_s3data')


    models = {
        u'main.s3data': {
            'Meta': {'object_name': 'S3Data'},
            'bucket': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['main']