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
from action.serializers import CommentSerializer, ReCommentSerializer, WinningDataSerializer
import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from account.models import WinningUser, WinningData
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

def comment(request):
    return render_to_response("action/comment.html", locals(), context_instance=RequestContext(request))

def get_winning(request):
    if request.user.is_authenticated():
        if request.user.socialaccount_set.all():
            fb_id = request.user.socialaccount_set.all()[0].extra_data["id"]
            pic_url = "http://graph.facebook.com/v2.8/%s/picture" % fb_id
            name = request.user.socialaccount_set.all()[0].extra_data["name"]
        else:
            pic_url = False
    else:
        pic_url = False

    if request.user.is_authenticated():
        try:
            winning = WinningUser.objects.get(user=request.user.id)
        except:
            no_get = True


    return render_to_response("action/get_winning.html", locals(), context_instance=RequestContext(request))

class CommentPostView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        留言
        """
        serializer = self.serializer_class(data=request.DATA)
        #import pdb;pdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            #import pdb;pdb.set_trace()
            #serializer = self.serializer_class(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WinningDataView(generics.GenericAPIView):
    serializer_class = WinningDataSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        登記領獎資料
        """
        serializer = self.serializer_class(data=request.DATA)
        #import pdb;pdb.set_trace()
        if serializer.is_valid():

            try:
                obj = WinningUser.objects.get(user=request.user)
                name = serializer.data.get('name')
                phone = serializer.data.get('phone')
                address = serializer.data.get('address')
                print phone
                try:
                    data = WinningData.objects.get(name=name)
                    data.phone = phone
                    data.address = address
                    data.prize = obj.prize
                    data.save()
                except:
                    data = WinningData(name=name, phone=phone, address=address, prize=obj.prize)
                    data.save()
            except:
                return Response(u"您沒有中獎", status=status.HTTP_200_OK)



            return Response(u"以完成登記", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReCommentPostView(generics.GenericAPIView):
    serializer_class = ReCommentSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        回復留言
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            #import pdb;pdb.set_trace()
            #serializer = self.serializer_class(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
