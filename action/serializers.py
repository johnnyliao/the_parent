#-*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from action.models import Comment, ReComment

from rest_framework import serializers

from datetime import datetime,timedelta
from django.utils import timezone
import urlparse
from django.contrib.sites.models import Site

class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment

class ReCommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = ReComment

class WinningDataSerializer(serializers.Serializer):
	name = serializers.CharField()
	phone = serializers.IntegerField()
	address = serializers.CharField()
