#-*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from account.models import User
from allauth.socialaccount.models import (SocialLogin, SocialToken, SocialAccount)
from rest_framework import serializers

from django.contrib.auth import get_user_model
import pytz
from datetime import datetime, timedelta

class FacebookConnectSerializer(serializers.Serializer):
    access_token = serializers.CharField()

class UserInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = User

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