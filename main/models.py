#-*- encoding: utf-8 -*-

from django.contrib.auth.models import AbstractUser

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.contenttypes import generic

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.sites.models import Site

import urlparse, settings
from cart.models import Brand
from django.utils import simplejson


class S3Data(models.Model):
	key = models.CharField(_(u"acckey"), max_length=60)
	bucket = models.CharField(_(u"bucket"), max_length=100)


class BrandIndexBanner(models.Model):
    banner = models.ImageField(_(u"banner"), upload_to='main/brand_banner')
    name = models.CharField(_(u"Banner名稱"), max_length=30)
    link = models.CharField(_(u"Banner連結"), max_length=200)

    def __unicode__(self):
        return self.name

    def image_tag(self):
        return '<img style="width:100px;height:100px" src="' + self.banner.url + '" />'

    class Meta:
        verbose_name = _(u"首頁Banner資訊")
        verbose_name_plural = _(u"首頁Banner列表")

class BrandIndexMovie(models.Model):
    link = models.CharField(_(u"連結"), max_length=100)
    name = models.CharField(_(u"影片名稱"), max_length=30)
    photo = models.ImageField(_(u"預覽圖"), upload_to='main/brand_index_movie_prview')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"首頁影片資訊")
        verbose_name_plural = _(u"首頁影片列表")

class BrandIndex(models.Model):
    banner = models.ManyToManyField("BrandIndexBanner", verbose_name=_(u"首頁banner"), related_name='brand_index_banner')
    movie = models.ManyToManyField("BrandIndexMovie", verbose_name=_(u"首頁影片"), related_name='brand_index_movie')
    brand = models.ManyToManyField(Brand, verbose_name=_(u"首頁商家"), related_name='index_brands')

    class Meta:
        verbose_name = _(u"商家首頁資訊")
        verbose_name_plural = _(u"商家首頁列表")
