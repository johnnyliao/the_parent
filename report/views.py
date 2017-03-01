#-*- encoding: utf-8 -*-
from report.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from report.serializers import addRegisterSerializer, DayInnerCountSerializer
from rest_framework import generics, status
import json, requests, urllib, urllib2, re, base64, os, datetime
import urlparse, time, cookielib, hashlib, time
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from selenium import webdriver
import platform
from datetime import timedelta
import MySQLdb
from dateutil import parser
import json
def register(request):

	return render_to_response("report/register.html", locals(), context_instance=RequestContext(request))

class AddInner(generics.GenericAPIView):
	serializer_class = addRegisterSerializer
	permission_classes = (AllowAny, )

	def post(self, request, format=None):
		"""
		增加文章
		"""
		serializer = self.serializer_class(data=request.DATA)
		if serializer.is_valid():
			name = serializer.data.get('name')
			inner_id = serializer.data.get('inner_id')
			db = MySQLdb.connect(host="188.166.233.109", user="foyoko_remote", passwd="Xc7YMW4tXRcEbUch", db="ttshow")
			cursor = db.cursor()
			sql = "SELECT `c_num_click` FROM page WHERE `page_id` = " + inner_id
			cursor.execute(sql)
			try:
				count = cursor.fetchall()[0][0]
			except:
				return Response({"result":False, "msg":u"文章ID輸入錯誤"})
			try:
				register = Register.objects.get(inner_id=inner_id, name=name)
				register.base_count = count
				register.save()
				return Response({"result":True, "msg":u"更新文章ID點擊數成功"})
			except ObjectDoesNotExist:
				try:
					register = Register(name=name, inner_id=inner_id, base_count=count)
					register.save()
					return Response({"result":True, "msg":u"新增文章ID成功"})
				except IntegrityError:
					return Response({"result":False, "msg":u"已經有相同的文章ID"})

#每日排程
def day_record(request):
	tia_inner = Register.objects.all().filter(name="TIA")
	amy_inner = Register.objects.all().filter(name="AMY")
	annie_inner = Register.objects.all().filter(name="ANNIE")
	zoey_inner = Register.objects.all().filter(name="ZOEY")
	mandy_inner = Register.objects.all().filter(name="MANDY")
	richard_inner = Register.objects.all().filter(name="RICHARD")
	get_new_hit_count(tia_inner, "TIA")
	get_new_hit_count(amy_inner, "AMY")
	get_new_hit_count(annie_inner, "ANNIE")
	get_new_hit_count(zoey_inner, "ZOEY")
	get_new_hit_count(mandy_inner, "MANDY")
	get_new_hit_count(richard_inner, "RICHARD")

	return HttpResponse("OK")

def get_new_hit_count(register_list, name):
	for item in register_list:
		db = MySQLdb.connect(host="188.166.233.109", user="foyoko_remote", passwd="Xc7YMW4tXRcEbUch", db="ttshow")
		cursor = db.cursor()
		sql = "SELECT `c_num_click` FROM page WHERE `page_id` = " + item.inner_id
		cursor.execute(sql)
		try:
			count = cursor.fetchall()[0][0]
		#import pdb;pdb.set_trace()
			day_count = DayInnerCount(name=name, hit_count=count, register=item)
			day_count.save()
		except:
			continue

#每日排程 計算成長值
def day_group_up(request):
	tia_inner_id = Register.objects.all().filter(name="TIA")
	amy_inner_id = Register.objects.all().filter(name="AMY")
	annie_inner_id  = Register.objects.all().filter(name="ANNIE")
	zoey_inner_id  = Register.objects.all().filter(name="ZOEY")
	mandy_inner_id  = Register.objects.all().filter(name="MANDY")
	richard_inner_id  = Register.objects.all().filter(name="RICHARD")
	get_group_by_name_inner_id(tia_inner_id, "TIA")
	get_group_by_name_inner_id(amy_inner_id, "AMY")
	get_group_by_name_inner_id(annie_inner_id, "ANNIE")
	get_group_by_name_inner_id(zoey_inner_id, "ZOEY")
	get_group_by_name_inner_id(mandy_inner_id, "MANDY")
	get_group_by_name_inner_id(richard_inner_id, "RICHARD")
	return HttpResponse("OK")

def get_group_by_name_inner_id(id_list, name):
	for item in id_list:

		get_group_up(item.every_day_data.all().order_by("-date")[::-1], item.base_count)

def get_group_up(every_day, base_count):
	pre_click_count = 0

	for item in every_day:
		if pre_click_count == 0:
			item.group = (item.hit_count - base_count)
			item.save()
			pre_click_count = item.hit_count
		else:
			#item.talk_about_is_group = (item.talk_about_is - pre_talk_about_is) / (pre_talk_about_is + 0.0) * 100
			item.group = (item.hit_count - pre_click_count)
			item.save()
			pre_click_count = item.hit_count


def group_report(request):
	name = request.GET.get("name", "TIA")

	inner_id_list = Register.objects.all().filter(name=name)
	inner_id_list = DayInnerCount.objects.all().filter(register__name=name)
	print inner_id_list
	"""
	amy_inner_id = Register.objects.all().filter(name="AMY")
	annie_inner_id  = Register.objects.all().filter(name="ANNIE")
	zoey_inner_id  = Register.objects.all().filter(name="ZOEY")
	mandy_inner_id  = Register.objects.all().filter(name="MANDY")
	richard_inner_id  = Register.objects.all().filter(name="RICHARD")
	"""

	return render_to_response("report/group_report.html", locals(), context_instance=RequestContext(request))

def get_report(request):
	name = request.GET.get("name", "TIA")
	start_date = request.GET.get("start", datetime.date.today())
	end_date = request.GET.get("end", datetime.date.today())
	start_date = parser.parse(start_date)
	end_date = parser.parse(end_date)
	inner_id_list = DayInnerCount.objects.all().filter(register__name=name, date__gte=start_date, date__lte=end_date)

	seralizer = DayInnerCountSerializer(inner_id_list, many=True)

	return HttpResponse(json.dumps(seralizer.data))

def return_each_data(inner_id_list, name):
	result = {}
	for obj in inner_id_list:
		data_list = DayInnerCount.objects.filter(inner_id=item.inner_id, name=name).order_by("-date")[:8][::-1]

		for item in data_list:
			date_result = []
			record = DayInnerCount.objects.filter(inner_id=item.inner_id, name=name).order_by("-date")[:7][::-1]
			date_result.append({"inner_id":item.inner_id, "record":record})

	result[name] = date_result

	return result