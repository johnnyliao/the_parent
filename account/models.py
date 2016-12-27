#-*- encoding: utf-8 -*-

from django.contrib.auth.models import AbstractUser

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.contenttypes import generic

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.sites.models import Site

import urlparse, settings

from django.utils import simplejson



class User(AbstractUser):
	nickname = models.CharField(_(u"名稱"), max_length=30, default="", null=True, blank=True)
	phone_number = models.CharField(_(u"電話號碼"), max_length=30, default="", null=True, blank=True)
	photo = models.ImageField(upload_to='photos', max_length=255, null=True, blank=True)

