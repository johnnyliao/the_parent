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


class S3Data(models.Model):
	key = models.CharField(_(u"acckey"), max_length=60)
	bucket = models.CharField(_(u"bucket"), max_length=100)
