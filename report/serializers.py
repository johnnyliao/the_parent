#-*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from report.models import Register

from rest_framework import serializers

from datetime import datetime,timedelta
from django.utils import timezone
import urlparse
from django.contrib.sites.models import Site

class addRegisterSerializer(serializers.Serializer):
	name = serializers.CharField()
	inner_id = serializers.CharField()
