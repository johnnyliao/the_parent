#-*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from account.models import User, UserViewLog
from allauth.socialaccount.models import (SocialLogin, SocialToken, SocialAccount)
from rest_framework import serializers

from django.contrib.auth import get_user_model
import pytz
from datetime import datetime, timedelta

class FacebookConnectSerializer(serializers.Serializer):
    access_token = serializers.CharField()

class UserInfoSerializer(serializers.ModelSerializer):
	user_img = serializers.SerializerMethodField('get_user_img')

	class Meta:
		model = User

	def get_user_img(self, user):
		if user.socialaccount_set.all():
			fb_id = user.socialaccount_set.all()[0].extra_data["id"]
			pic_url = "http://graph.facebook.com/v2.8/%s/picture" % fb_id
			return pic_url
		else:
			return "/static/img/person-icon.png"

class UserViewLoSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserViewLog

	def update(self, instance, validated_data):
		instance.user = validated_data.get('user', instance.user)
		instance.product = validated_data.get('product', instance.product)
		instance.save()
		return instance

class UserWinningSerializer(serializers.Serializer):
	winning_type = serializers.CharField()
	count = serializers.IntegerField()

class UserRegisterSerializer(serializers.Serializer):
	username = serializers.CharField()
	nickname = serializers.CharField()
	password = serializers.CharField()
	city = serializers.CharField()
	district = serializers.CharField()
	phone_number = serializers.CharField()
	year = serializers.DecimalField()
	sex = serializers.CharField()
	address = serializers.CharField()
	birthday = serializers.DateTimeField()

class UserModifySerializer(serializers.Serializer):
	username = serializers.CharField()
	email = serializers.CharField(blank=True)
	nickname = serializers.CharField()
	city = serializers.CharField()
	district = serializers.CharField()
	phone_number = serializers.CharField()
	year = serializers.DecimalField()
	sex = serializers.CharField()
	address = serializers.CharField()
	birthday = serializers.DateTimeField()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField()
	new_password = serializers.CharField()
	confirm_password = serializers.CharField()

class UserForgetPasswordSerializer(serializers.Serializer):
	username = serializers.CharField()