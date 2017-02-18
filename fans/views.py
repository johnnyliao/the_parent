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

class get_fans(APIView):
	#serializer_class = FansPageSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		"""
        取得粉絲頁資訊
        fans_type -- 粉絲頁名稱
        """
		fans_type = request.QUERY_PARAMS.get('fans_type')
		chrome_path = "C:\chrome_driver\chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
		phantomjs = "/home/ubuntu/phantomjs" #chromedriver.exe執行檔所存在的路徑
		if platform.system() == "Windows":
			web = webdriver.Chrome(chrome_path)
		else:
			web = webdriver.PhantomJS(phantomjs)

		fburl = "https://www.facebook.com/pg/"+fans_type+"/likes/?ref=page_internal"
		web.get(fburl)

		talk_about_is = web.find_elements_by_class_name("_50f6")[0].text
		total_like_count = web.find_elements_by_class_name("_50f6")[1].text
		total_fans = web.find_elements_by_class_name("_50f6")[3].text
		talk_about_is = process_number(talk_about_is)
		total_like_count = process_number(total_like_count)
		total_fans = process_number(total_fans)
		web.close()
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
		return Response(serializer.data)


def process_number(string):
	split_numbers = string.split(",")
	result = ""
	for item in split_numbers:
		result += item

	return int(result)