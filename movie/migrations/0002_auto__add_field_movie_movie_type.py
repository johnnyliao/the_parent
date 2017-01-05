# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Movie.movie_type'
        db.add_column(u'movie_movie', 'movie_type',
                      self.gf('django.db.models.fields.CharField')(default='family', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Movie.movie_type'
        db.delete_column(u'movie_movie', 'movie_type')


    models = {
        u'movie.movie': {
            'Meta': {'object_name': 'Movie'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'movie_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['movie']