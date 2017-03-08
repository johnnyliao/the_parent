#-*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from report.models import Register, DayInnerCount, ReportUser

from rest_framework import serializers

from datetime import datetime,timedelta
from django.utils import timezone
import urlparse
from django.contrib.sites.models import Site

class addRegisterSerializer(serializers.Serializer):
	name = serializers.CharField()
	inner_id = serializers.CharField()
	web_type = serializers.CharField()

class ReportUserDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = ReportUser


class DayInnerCountSerializer(serializers.ModelSerializer):
	date = serializers.SerializerMethodField('convert_date')
	class Meta:
		model = DayInnerCount

	def convert_date(self, obj):
		return obj.date.strftime("%Y-%m-%d")