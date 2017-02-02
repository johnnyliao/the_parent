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

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.sites.models import Site
import urlparse, settings

TYPE_CHOICES = (
	("new", u'最新發表'),
	("hot", u'熱門即時'),
	("brand", u'品牌合作'),
	("kuso", u'惡搞'),
	("love", u'放閃'),
	("family", u'親子家庭'),
)


class Movie(models.Model):
    link = models.CharField(_(u"youtube連結"), max_length=100)
    title = models.CharField(_(u"標題"), max_length=100)
    description = RichTextField(_(u"簡介"), max_length=2000)
    movie_type = models.CharField(_(u"分類"), max_length=100, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = _(u'影片')
        verbose_name_plural = _(u'影片列表')


