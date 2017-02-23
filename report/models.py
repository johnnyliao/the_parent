#-*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from account.models import *
from django.contrib.auth.models import AbstractUser
from mezzanine.core.fields import RichTextField
from django.utils import timezone

from django.contrib.contenttypes import generic
import datetime
from django.core.exceptions import ObjectDoesNotExist
#from account.models import User
from django.contrib.sites.models import Site
import urlparse, settings

NANE_CHOICES = (
    ("TIA", _(u'TIA')),
    ("AMY", _(u'AMY')),
    ("ANNIE", _(u'ANNIE')),
    ("ZOEY", _(u'ZOEY')),
    ("MANDY", _(u'MANDY')),
    ("RICHARD", _(u'RICHARD')),
)

class Register(models.Model):
    name = models.CharField(_(u"人名"), choices=NANE_CHOICES, max_length=10)
    inner_id = models.CharField(_(u"文章id"), max_length=20, unique=True)
    base_count = models.IntegerField(_(u"基準點擊數"))
    date = models.DateTimeField(_(u"日期"), auto_now=True)

    class Meta:
        verbose_name = _(u"增加文章")
        verbose_name_plural = _(u"增加文章列表")

class DayInnerCount(models.Model):
    name = models.CharField(_(u"人名"), choices=NANE_CHOICES, max_length=10)
    register = models.ForeignKey(Register, related_name='every_day_data')
    hit_count = models.IntegerField(_(u"點擊數"))
    date = models.DateField(_(u"日期"))
    group = models.IntegerField(_(u"點擊成長數"), null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.date.today()
        super(DayInnerCount, self).save(*args, **kwargs)