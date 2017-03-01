# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WinningData.email'
        db.delete_column(u'account_winningdata', 'email')


    def backwards(self, orm):
        # Adding field 'WinningData.email'
        db.add_column(u'account_winningdata', 'email',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)


    models = {
        u'account.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'account.emailconfirmation': {
            'Meta': {'object_name': 'EmailConfirmation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.EmailAddress']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'account.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'account.usermovieviewlog': {
            'Meta': {'object_name': 'UserMovieViewLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_view_movie_logs'", 'to': u"orm['movie.Movie']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_movie_view_logs'", 'to': u"orm['account.User']"})
        },
        u'account.usermsg': {
            'Meta': {'object_name': 'UserMsg'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'msg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_msg_msg'", 'to': u"orm['account.Message']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_msgs'", 'to': u"orm['account.User']"})
        },
        u'account.userverify': {
            'Meta': {'object_name': 'UserVerify'},
            'active_minutes': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'date_verified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'verify'", 'unique': 'True', 'to': u"orm['account.User']"}),
            'verification_hash': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'account.userviewlog': {
            'Meta': {'object_name': 'UserViewLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_view_product_logs'", 'to': u"orm['cart.ProductInfo']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_view_logs'", 'to': u"orm['account.User']"})
        },
        u'account.winningdata': {
            'Meta': {'object_name': 'WinningData'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'prize': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'account.winninguser': {
            'Meta': {'object_name': 'WinningUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prize': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_winnging'", 'to': u"orm['account.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'cart.brand': {
            'Meta': {'object_name': 'Brand'},
            'banner': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brand_banner'", 'symmetrical': 'False', 'to': u"orm['cart.BrandBanner']"}),
            'brand_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'movie': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brand_movie'", 'symmetrical': 'False', 'to': u"orm['cart.BrandMovie']"})
        },
        u'cart.brandbanner': {
            'Meta': {'object_name': 'BrandBanner'},
            'banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'cart.brandmovie': {
            'Meta': {'object_name': 'BrandMovie'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'cart.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'cart.productinfo': {
            'Meta': {'object_name': 'ProductInfo'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_brand'", 'to': u"orm['cart.Brand']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_stock': ('django.db.models.fields.IntegerField', [], {}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'product_images'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cart.ProductImage']"}),
            'ship_day': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ship_way': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.IntegerField', [], {}),
            'trade_desc': ('mezzanine.core.fields.RichTextField', [], {'max_length': '2000'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'video_link': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'video_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'movie.movie': {
            'Meta': {'object_name': 'Movie'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('mezzanine.core.fields.RichTextField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'movie_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']