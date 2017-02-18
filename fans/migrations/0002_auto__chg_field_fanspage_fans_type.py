# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FansPage.fans_type'
        db.alter_column(u'fans_fanspage', 'fans_type', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):

        # Changing field 'FansPage.fans_type'
        db.alter_column(u'fans_fanspage', 'fans_type', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'fans.fanspage': {
            'Meta': {'object_name': 'FansPage'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'fans_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'talk_about_is': ('django.db.models.fields.IntegerField', [], {}),
            'total_fans': ('django.db.models.fields.IntegerField', [], {}),
            'total_like_count': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['fans']