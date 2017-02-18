# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FansPage.talk_about_is_group'
        db.add_column(u'fans_fanspage', 'talk_about_is_group',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FansPage.total_like_count_group'
        db.add_column(u'fans_fanspage', 'total_like_count_group',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FansPage.total_fans_group'
        db.add_column(u'fans_fanspage', 'total_fans_group',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FansPage.talk_about_is_group'
        db.delete_column(u'fans_fanspage', 'talk_about_is_group')

        # Deleting field 'FansPage.total_like_count_group'
        db.delete_column(u'fans_fanspage', 'total_like_count_group')

        # Deleting field 'FansPage.total_fans_group'
        db.delete_column(u'fans_fanspage', 'total_fans_group')


    models = {
        u'fans.fanspage': {
            'Meta': {'object_name': 'FansPage'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'fans_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'talk_about_is': ('django.db.models.fields.IntegerField', [], {}),
            'talk_about_is_group': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_fans': ('django.db.models.fields.IntegerField', [], {}),
            'total_fans_group': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_like_count': ('django.db.models.fields.IntegerField', [], {}),
            'total_like_count_group': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['fans']