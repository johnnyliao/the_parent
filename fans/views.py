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
		talk_about_is = request.QUERY_PARAMS.get('talk_about_is')
		total_like_count = request.QUERY_PARAMS.get('total_like_count')
		total_fans = request.QUERY_PARAMS.get('total_fans')

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