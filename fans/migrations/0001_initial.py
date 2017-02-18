# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FansPage'
        db.create_table(u'fans_fanspage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk_about_is', self.gf('django.db.models.fields.IntegerField')()),
            ('total_like_count', self.gf('django.db.models.fields.IntegerField')()),
            ('total_fans', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('fans_type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'fans', ['FansPage'])


    def backwards(self, orm):
        # Deleting model 'FansPage'
        db.delete_table(u'fans_fanspage')


    models = {
        u'fans.fanspage': {
            'Meta': {'object_name': 'FansPage'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'fans_type': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'talk_about_is': ('django.db.models.fields.IntegerField', [], {}),
            'total_fans': ('django.db.models.fields.IntegerField', [], {}),
            'total_like_count': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['fans']