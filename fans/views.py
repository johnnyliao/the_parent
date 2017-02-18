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
		fans = FansPage.objects.get(date=datetime.date.today())
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