#-*- encoding: utf-8 -*-
from fans.models import FansPage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from fans.serializers import FansPageSerializer
from rest_framework import generics, status
import json, requests, urllib, urllib2, re, base64, os, datetime
import urlparse, time, cookielib, hashlib, time
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from selenium import webdriver
import platform
from datetime import timedelta

def get_fans(request):
	"""
    取得粉絲頁資訊
    fans_type -- 粉絲頁名稱
    talk_about_is -- 粉絲頁名稱
    total_like_count -- 粉絲頁名稱
    total_fans -- 粉絲頁名稱
    """
	fans_type = request.GET.get('fans_type')
	talk_about_is = request.GET.get('talk_about_is')
	total_like_count = request.GET.get('total_like_count')
	total_fans = request.GET.get('total_fans')

	try:
		fans = FansPage.objects.get(date=datetime.date.today(), fans_type=fans_type)
		fans.total_fans = total_fans
		fans.total_like_count = total_like_count
		fans.talk_about_is = talk_about_is
		fans.fans_type = fans_type
	except:
		fans = FansPage(talk_about_is=talk_about_is, total_like_count=total_like_count, total_fans=total_fans, fans_type=fans_type)

	fans.save()
	serializer = FansPageSerializer(fans)
	print serializer.data
	return HttpResponse(serializer.data)


def process_number(string):
	split_numbers = string.split(",")
	result = ""
	for item in split_numbers:
		result += item

	return int(result)

def fans_report(request):
	wwwttshow = FansPage.objects.filter(fans_type="wwwttshow").order_by("-date").order_by("-date")[:7][::-1]
	ttshowpet = FansPage.objects.filter(fans_type="ttshowpet").order_by("-date").order_by("-date")[:7][::-1]
	draw_fans = FansPage.objects.filter(fans_type="draw.fans").order_by("-date").order_by("-date")[:7][::-1]
	TTShowMusic = FansPage.objects.filter(fans_type="TTShowMusic").order_by("-date").order_by("-date")[:7][::-1]
	GoodNews_FANS = FansPage.objects.filter(fans_type="GoodNews.FANS").order_by("-date").order_by("-date")[:7][::-1]

	data =[
		{"name":u"台灣達人秀", "data":wwwttshow, "week":week_report_handle("wwwttshow"), "month":month_report_handle("wwwttshow")},
		{"name":u"達人秀寵物", "data":ttshowpet, "week":week_report_handle("ttshowpet"), "month":month_report_handle("ttshowpet")},
		{"name":u"達人秀插畫", "data":draw_fans, "week":week_report_handle("draw.fans"), "month":month_report_handle("draw.fans")},
		{"name":u"達人秀音樂", "data":TTShowMusic, "week":week_report_handle("TTShowMusic"), "month":month_report_handle("TTShowMusic")},
		{"name":u"達人秀趣味新聞", "data":GoodNews_FANS, "week":week_report_handle("GoodNews.FANS"), "month":month_report_handle("GoodNews.FANS")},
	]

	print data[0]["week"]
	return render_to_response("fans/fans_report.html", locals(), context_instance=RequestContext(request))


def group_up(request):
	wwwttshow = FansPage.objects.filter(fans_type="wwwttshow").order_by("-date")[:8][::-1]
	ttshowpet = FansPage.objects.filter(fans_type="ttshowpet").order_by("-date")[:8][::-1]
	draw_fans = FansPage.objects.filter(fans_type="draw.fans").order_by("-date")[:8][::-1]
	TTShowMusic = FansPage.objects.filter(fans_type="TTShowMusic").order_by("-date")[:8][::-1]
	GoodNews_FANS = FansPage.objects.filter(fans_type="GoodNews.FANS").order_by("-date")[:8][::-1]
	#import pdb;pdb.set_trace()
	group_up_handle(wwwttshow)
	group_up_handle(ttshowpet)
	group_up_handle(draw_fans)
	group_up_handle(TTShowMusic)
	group_up_handle(GoodNews_FANS)
	return HttpResponse("ok")

def group_up_handle(data):
	pre_talk_about_is = 0
	pre_total_like_count = 0
	pre_total_fans = 0
	for item in data:
		print item.date
		if pre_talk_about_is == 0:
			item.talk_about_is_group = 0
			item.total_like_count_group = 0
			item.total_fans_group = 0
			item.save()
			pre_talk_about_is = item.talk_about_is
			pre_total_like_count = item.total_like_count
			pre_total_fans = item.total_fans
		else:
			item.talk_about_is_group = (item.talk_about_is - pre_talk_about_is) / (pre_talk_about_is + 0.0) * 100
			item.total_like_count_group = (item.total_like_count - pre_total_like_count) / (pre_total_like_count +0.0) * 100
			item.total_fans_group = (item.total_fans - pre_total_fans) / (pre_total_fans + 0.0) * 100
			item.save()
			pre_talk_about_is = item.talk_about_is
			pre_total_like_count = item.total_like_count
			pre_total_fans = item.total_fans


def week_report_handle(fans_type):
	last_week=datetime.date.today()-timedelta(days=7)
	#import pdb;pdb.set_trace()
	#fans_list = ["wwwttshow", "ttshowpet", "draw.fans", "TTShowMusic", "GoodNews.FANS"]
	fans_pages = FansPage.objects.filter(fans_type=fans_type, date__gte=last_week, date__lte=datetime.date.today()).order_by("date")

	start = fans_pages[0]
	last = fans_pages[len(fans_pages) - 1]

	talk_about_is = (start.talk_about_is - last.talk_about_is) / (last.talk_about_is + 0.0) * 100
	total_like_count = (start.total_like_count - last.total_like_count) / (last.total_like_count + 0.0) * 100
	total_fans = (start.total_fans - last.total_fans) / (last.total_fans + 0.0) * 100

	return {"talk_about_is":talk_about_is, "total_like_count":total_like_count, "total_fans":total_fans, "start":start.date, "last":last.date}


def month_report_handle(fans_type):
	last_week=datetime.date.today()-timedelta(days=30)
	#import pdb;pdb.set_trace()
	#fans_list = ["wwwttshow", "ttshowpet", "draw.fans", "TTShowMusic", "GoodNews.FANS"]
	fans_pages = FansPage.objects.filter(fans_type=fans_type, date__gte=last_week, date__lte=datetime.date.today()).order_by("date")

	start = fans_pages[0]
	last = fans_pages[len(fans_pages) - 1]

	talk_about_is = (start.talk_about_is - last.talk_about_is) / (last.talk_about_is + 0.0) * 100
	total_like_count = (start.total_like_count - last.total_like_count) / (last.total_like_count + 0.0) * 100
	total_fans = (start.total_fans - last.total_fans) / (last.total_fans + 0.0) * 100

	return {"talk_about_is":talk_about_is, "total_like_count":total_like_count, "total_fans":total_fans, "start":start.date, "last":last.date}

