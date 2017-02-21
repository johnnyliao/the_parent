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
#from account.models import User
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
    photo = models.ImageField(_(u"預覽圖"), upload_to='main/video_pre_image')
    date = models.DateTimeField(_(u"加入時間"), auto_now=True)

    class Meta:
        verbose_name = _(u'影片')
        verbose_name_plural = _(u'影片列表')

    def __unicode__(self):
        return self.title

    def image_tag(self):
        return '<img style="width:100px;height:100px" src="' + self.photo.url + '" />'

    image_tag.allow_tags = True

class Comment(models.Model):
    user = models.ForeignKey("account.User", related_name='user_movie_comment')
    content = models.CharField(_(u"影片留言內容"), max_length=100)
    date = models.DateTimeField(_(u"影片留言時間"), auto_now=True)
    movie = models.ForeignKey(Movie, related_name='movie_comments')

    class Meta:
        verbose_name = _(u'影片留言')
        verbose_name_plural = _(u'影片留言列表')

    def __unicode__(self):
        return self.content

class ReComment(models.Model):
    user = models.ForeignKey("account.User", related_name='user_movie_re_comment')
    content = models.CharField(_(u"影片留言內容"), max_length=100)
    date = models.DateTimeField(_(u"影片留言時間"), auto_now=True)
    re_comment = models.ForeignKey(Comment, related_name='movie_re_comments')

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = _(u'影片回覆留言')
        verbose_name_plural = _(u'影片回覆留言列表')
