#-*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from movie.models import Comment, ReComment
from account.serializers import UserInfoSerializer
from rest_framework import serializers
from datetime import datetime,timedelta
from django.utils import timezone
import urlparse
from django.contrib.sites.models import Site

class CommentSerializer(serializers.ModelSerializer):
	like = serializers.IntegerField(required=False)
	class Meta:
		model = Comment

class ReCommentSerializer(serializers.ModelSerializer):
	like = serializers.IntegerField(required=False)
	class Meta:
		model = ReComment

class CommentLikeSerializer(serializers.Serializer):
	comment_id = serializers.IntegerField()
	comment_type = serializers.CharField()

class VideoLikeSerializer(serializers.Serializer):
	video_id = serializers.IntegerField()

class ReCommentWebSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()

	class Meta:
		model = ReComment

class CommentWebSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()

	class Meta:
		model = Comment