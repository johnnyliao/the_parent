#-*- encoding: utf-8 -*-

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer


import urllib, urllib2, json, simplejson

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.middleware.csrf import get_token

import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from allauth.socialaccount.providers.facebook.views import fb_complete_login

from allauth.socialaccount.providers.twitter.provider import TwitterProvider
from allauth.socialaccount.providers.twitter.views import TwitterAPI

from allauth.socialaccount.providers.weibo.provider import WeiboProvider

from allauth.socialaccount.models import (SocialLogin, SocialToken, SocialAccount)
from allauth.socialaccount.helpers import complete_social_login, render_authentication_error

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import settings, random
from account.models import User, UserVerify
from rest_framework.views import APIView
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from datetime import datetime, timedelta
from main.models import BrandIndex, BrandIndexBanner, BrandIndexMovie
from django.db.models import Q
import pytz
from allauth.socialaccount.models import *

def home(request):
	return render_to_response("main/page_coming_soon2.html", locals(), context_instance=RequestContext(request))

def login(request):
	return render_to_response("main/login.html", locals(), context_instance=RequestContext(request))

def register(request):
	return render_to_response("main/register.html", locals(), context_instance=RequestContext(request))

def index(request):
	brand_index = BrandIndex.objects.all()[0]

	return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

def forget_password(request):
	if is_social_account(request.user):
		social_account = "yes"
	else:
		social_account = "no"
	return render_to_response("main/forgetPassword.html", locals(), context_instance=RequestContext(request))

@login_required
def member(request):
	user = request.user
	birthday = str(user.birthday).split(' ')[0]
	return render_to_response("main/member.html", locals(), context_instance=RequestContext(request))

@login_required
def change_password(request):
	if is_social_account(request.user):
		social_account = "yes"
	else:
		social_account = "no"

	return render_to_response("main/changePassword.html", locals(), context_instance=RequestContext(request))

@login_required
def register_success(request):
	user = request.user
	if user.is_verified():
		user = request.user
		birthday = str(user.birthday).split(' ')[0]
		return render_to_response("main/member.html", locals(), context_instance=RequestContext(request))
	else:
		try:
			UserVerify.objects.get(user=request.user)
			print "user verify resend_verify_code"
			request.user.verify.resend_verify_code()

			return render_to_response("main/regSuccess.html", locals(), context_instance=RequestContext(request))
		except:
			user_verify = UserVerify.objects.create(user=request.user)
			print "user verify create"
		print "veiw end!!!!"
		return render_to_response("main/regSuccess.html", locals(), context_instance=RequestContext(request))


def is_social_account(user):
	try:
		user = SocialAccount.objects.get(user_id=user.id)
		return True
	except:
		return False