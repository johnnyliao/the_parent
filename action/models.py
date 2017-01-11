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
import urlparse, settings


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comment')
    content = models.CharField(_(u"留言內容"), max_length=100)
    date = models.DateTimeField(_(u"留言時間"), auto_now=True)

    class Meta:
        verbose_name = _(u'留言')
        verbose_name_plural = _(u'留言列表')

class ReComment(models.Model):
    user = models.ForeignKey(User, related_name='user_re_comment')
    content = models.CharField(_(u"留言內容"), max_length=100)
    date = models.DateTimeField(_(u"留言時間"), auto_now=True)
    re_comment = models.ForeignKey(Comment, related_name='re_comment')



