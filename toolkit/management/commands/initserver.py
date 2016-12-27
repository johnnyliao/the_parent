# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.core.management import call_command
import settings
import random

from mezzanine.utils.models import get_user_model
User = get_user_model()

from autofixture import AutoFixture

from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            tables = connection.introspection.table_names()

            if len(tables) > 0:
                print 'Dropping tables ...'
                cursor = connection.cursor()
                cursor.execute('set foreign_key_checks = 0;')
                for table in connection.introspection.table_names():
                    print 'Dropping table ', table
                    cursor.execute('DROP TABLE ' + table)
                cursor.execute('set foreign_key_checks = 1;')
                transaction.commit_unless_managed()
                print ""
        except:
            pass

        call_command("createdb", interactive=False)
        if not settings.DEBUG:
            User.objects.create_superuser('admin', 'example@example.com.tw', '123456')
            print "Creating default account (username: admin / password: 123456) ..."

        print "Start loading default datas ..."


        # 會影響檔案圖片等絕對網址
        site = Site.objects.get_current()
        site.domain = 'http://127.0.0.1:8000/'
        site.save()

