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

from django.contrib.auth import authenticate, login, logout
import settings, random

from rest_framework.views import APIView
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from datetime import datetime, timedelta
from django.db.models import Q
import pytz

def home(request):
	return render_to_response("main/page_coming_soon2.html", locals(), context_instance=RequestContext(request))

def index(request):
	return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

def index1(request):
	return render_to_response("main/index1.html", locals(), context_instance=RequestContext(request))

def login(request):
	return render_to_response("main/shop-ui-login.html", locals(), context_instance=RequestContext(request))

def album(request):
	return render_to_response("main/index_album.html", locals(), context_instance=RequestContext(request))

def inner(request):
	return render_to_response("main/index_inner.html", locals(), context_instance=RequestContext(request))

def photo(request):
	return render_to_response("main/index_photo.html", locals(), context_instance=RequestContext(request))

def video(request):
	return render_to_response("main/index_video.html", locals(), context_instance=RequestContext(request))

def add_to_cart(request):
	return render_to_response("main/shop-ui-add-to-cart.html", locals(), context_instance=RequestContext(request))

def filter_list(request):
	return render_to_response("main/shop-ui-filter-list.html", locals(), context_instance=RequestContext(request))

def ui_inner(request):
	return render_to_response("main/shop-ui-inner.html", locals(), context_instance=RequestContext(request))

def register(request):
	return render_to_response("main/shop-ui-register.html", locals(), context_instance=RequestContext(request))
