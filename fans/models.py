#-*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from account.models import User
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

from django.contrib.contenttypes import generic

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.sites.models import Site
import urlparse, settings, datetime

FANS_PAGE_TYPE = (
    ("wwwttshow", _(u'台灣達人秀')),
    ("ttshowpet", _(u'達人秀寵物')),
    ("draw.fans", _(u'達人秀插畫')),
    ("TTShowMusic", _(u'達人秀音樂')),
    ("GoodNews.FANS", _(u'達人秀趣味新聞')),
)

class FansPage(models.Model):
    talk_about_is = models.IntegerField(_(u"談論這個的用戶"))
    talk_about_is_group = models.FloatField(_(u"談論這個的用戶成長率"), null=True, blank=True)
    total_like_count_group = models.FloatField(_(u"粉絲專頁按讚總數成長率"), null=True, blank=True)
    total_fans_group = models.FloatField(_(u"粉絲專頁粉絲總人數成長率"), null=True, blank=True)
    total_like_count = models.IntegerField(_(u"粉絲專頁按讚總數"))
    total_fans = models.IntegerField(_(u"粉絲專頁粉絲總人數"))
    date = models.DateField()
    fans_type = models.CharField(_(u"粉絲頁"), max_length=20, choices=FANS_PAGE_TYPE)

    class Meta:
        verbose_name = _(u'留言')
        verbose_name_plural = _(u'留言列表')

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.date.today()
        super(FansPage, self).save(*args, **kwargs)
