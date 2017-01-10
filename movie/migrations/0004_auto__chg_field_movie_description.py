# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Movie.description'
        db.alter_column(u'movie_movie', 'description', self.gf('mezzanine.core.fields.RichTextField')(max_length=2000))

    def backwards(self, orm):

        # Changing field 'Movie.description'
        db.alter_column(u'movie_movie', 'description', self.gf('django.db.models.fields.CharField')(max_length=2000))

    models = {
        u'movie.movie': {
            'Meta': {'object_name': 'Movie'},
            'description': ('mezzanine.core.fields.RichTextField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'movie_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['movie']