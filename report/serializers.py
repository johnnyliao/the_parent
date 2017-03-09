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
	title = serializers.SerializerMethodField('get_title')
	web_type = serializers.SerializerMethodField('get_type')

	class Meta:
		model = DayInnerCount

	def convert_date(self, obj):
		return obj.date.strftime("%Y-%m-%d")

	def get_title(self, obj):
		return obj.register.title

	def get_type(self, obj):
		return obj.register.web_type