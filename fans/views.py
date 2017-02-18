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
	wwwttshow = FansPage.objects.filter(fans_type="wwwttshow").order_by("-date").reverse()[:7]
	ttshowpet = FansPage.objects.filter(fans_type="ttshowpet").order_by("-date").reverse()[:7]
	draw_fans = FansPage.objects.filter(fans_type="draw.fans").order_by("-date").reverse()[:7]
	TTShowMusic = FansPage.objects.filter(fans_type="TTShowMusic").order_by("-date").reverse()[:7]
	GoodNews_FANS = FansPage.objects.filter(fans_type="GoodNews.FANS").order_by("-date").reverse()[:7]
	data =[
		{"name":u"台灣達人秀", "data":wwwttshow},
		{"name":u"達人秀寵物", "data":ttshowpet},
		{"name":u"達人秀插畫", "data":draw_fans},
		{"name":u"達人秀音樂", "data":TTShowMusic},
		{"name":u"達人秀趣味新聞", "data":GoodNews_FANS},
	]

	return render_to_response("fans/fans_report.html", locals(), context_instance=RequestContext(request))

def group_up(request):
	wwwttshow = FansPage.objects.filter(fans_type="wwwttshow").order_by("-date").reverse()[:8]
	ttshowpet = FansPage.objects.filter(fans_type="ttshowpet").order_by("-date").reverse()[:8]
	draw_fans = FansPage.objects.filter(fans_type="draw.fans").order_by("-date").reverse()[:8]
	TTShowMusic = FansPage.objects.filter(fans_type="TTShowMusic").order_by("-date").reverse()[:8]
	GoodNews_FANS = FansPage.objects.filter(fans_type="GoodNews.FANS").order_by("-date").reverse()[:8]
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
		print "\n\n\n"
		print pre_talk_about_is
		print pre_total_like_count
		print pre_total_fans
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
			print "save data"
			print item.talk_about_is_group
			print item.total_like_count_group
			print item.total_fans_group
			pre_talk_about_is = item.talk_about_is
			pre_total_like_count = item.total_like_count
			pre_total_fans = item.total_fans

