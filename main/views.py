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
from cart.models import CartItem, PayMentRecord
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import settings, random
from account.models import User, UserVerify
from cart.models import Brand, ProductInfo
from rest_framework.views import APIView
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from datetime import datetime, timedelta
from main.models import BrandIndex, BrandIndexBanner, BrandIndexMovie
from django.db.models import Q
import pytz
from allauth.socialaccount.models import *
from account.views import login as main_login

def home(request):
	brand_index = BrandIndex.objects.all()[0]

	return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

def login(request):
	return render_to_response("main/login.html", locals(), context_instance=RequestContext(request))

def register(request):
	return render_to_response("main/register.html", locals(), context_instance=RequestContext(request))

@login_required
def pay_success(request):
	records = PayMentRecord.objects.filter(user=request.user)
	return render_to_response("main/pay_success.html", locals(), context_instance=RequestContext(request))

def cart_final(request):
	username = request.POST.get("username")
	ship_time = request.POST.get("ship_time")
	if ship_time == "morning":
		ship_time_tw = u"早上"
	elif ship_time == "afternoon":
		ship_time_tw = u"下午"
	elif ship_time == "night":
		ship_time_tw = u"晚上"
	choose_payment = request.POST.get("choose_payment")

	if choose_payment == "Credit":
		choose_payment_tw = u"信用卡"
	elif choose_payment == "CVS":
		choose_payment_tw = u"超商代碼"
	elif choose_payment == "ATM":
		choose_payment_tw = u"ATM"

	phone_number = request.POST.get("phone_number")
	city = request.POST.get("city")
	district = request.POST.get("district")
	address = request.POST.get("address")
	invoice_type = request.POST.get("invoice_type")

	if invoice_type == "1":
		invoice_type_tw = u"捐贈"
	elif invoice_type == "2":
		invoice_type_tw = u"二聯式"
	elif invoice_type == "3":
		invoice_type_tw = u"三聯式"

	invoice_kind = request.POST.get("invoice_kind")
	carruer_type = request.POST.get("carruer_type")

	if carruer_type == "1":
		carruer_type_tw = u"沒有載具"
	elif carruer_type == "2":
		carruer_type_tw = u"自然人憑證"
	elif carruer_type == "3":
		carruer_type_tw = u"手機條碼"

	love_code = request.POST.get("love_code")
	customer_identifier = request.POST.get("customer_identifier")
	customer_name = request.POST.get("customer_name")
	customer_addr = request.POST.get("customer_addr")
	customer_phone = request.POST.get("customer_phone")
	customer_email = request.POST.get("customer_email")


	return render_to_response("main/cart_final.html", locals(), context_instance=RequestContext(request))

def index(request):
	brand_index = BrandIndex.objects.all()[0]

	return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

def cart_check(request):
	brand_index = BrandIndex.objects.all()[0]

	return render_to_response("main/cart_check.html", locals(), context_instance=RequestContext(request))

def now_cart(request):
	if not request.user.is_authenticated():
		return redirect(main_login)

	product_id = request.GET.get("product_id")
	cart_items = request.user.user_cart_item.all().filter(is_checked=False)
	total_count = cart_items.count()
	red_bag = 0
	total_price = 0
	for item in cart_items:
		red_bag += item.amount
		total_price += item.amount * item.product.total_amount
	return render_to_response("main/now_cart.html", locals(), context_instance=RequestContext(request))

def product_detail(request, pk):
	#product_id = request.GET.get("product_id")
	#import pdb;pdb.set_trace()
	product_obj = ProductInfo.objects.get(id=pk)
	you_like = ProductInfo.objects.exclude(id=pk)
	if request.user.is_authenticated():
		cart_items = request.user.user_cart_item.all().filter(is_checked=False)
		total_count = cart_items.count()
	else:
		total_count = 0
	return render_to_response("main/product_detail.html", locals(), context_instance=RequestContext(request))

def indexshop(request):
	brand_id = request.GET.get("brand_id")
	brand_id1 = int(brand_id)
	brand_obj = Brand.objects.get(id=brand_id)
	brand_index = BrandIndex.objects.all()[0]
	print brand_id
	return render_to_response("main/index_shop.html", locals(), context_instance=RequestContext(request))

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
		return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))
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