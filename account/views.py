#-*- encoding: utf-8 -*-

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from account.models import User
from account.serializers import FacebookConnectSerializer, UserInfoSerializer, UserLoginSerializer, UserRegisterSerializer

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

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        建立 網站 帳號或是登入帳號為email格式
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            try:
                try:
                    User.objects.get(username=username)
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                    else:
                        return Response("401")
                        return Response("Bad username or password.", status=status.HTTP_401_UNAUTHORIZED)
                except User.DoesNotExist:
                    user = User.objects.create_user(username=username, password=password, email=username)
                    user = authenticate(username=username, password=password)
                    login(request, user)

                serializer = UserInfoSerializer(request.user, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.RequestException as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        註冊網站帳號或修改帳號資訊
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():

            username = serializer.data.get('username')
            password = serializer.data.get('password')
            re_password = serializer.data.get('re_password')
            phone_number = serializer.data.get('phone_number')
            year = serializer.data.get('year')
            sex = serializer.data.get('sex')
            email = serializer.data.get('email')
            address = serializer.data.get('address')
            birthday = serializer.data.get('birthday')
            if password != re_password:
                return Response("password wrong", status=status.HTTP_200_OK)
            try:
                try:
                    user = User.objects.get(username=username)
                    user.password = password
                    user.phone_number = phone_number
                    user.year = year
                    user.sex = sex
                    user.email = email
                    user.address = address
                    user.birthday = birthday
                    user.save()
                except User.DoesNotExist:
                    user = User(
                            username=username,
                            password=password,
                            phone_number=phone_number,
                            year=year,
                            sex=sex,
                            email=email,
                            address=address,
                            birthday=birthday
                        )
                    user.save()
                    user.backend = 'mezzanine.core.auth_backends.MezzanineBackend'
                    login(request, user)

                serializer = UserInfoSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.RequestException as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacebookConnectView(generics.GenericAPIView):
    serializer_class = FacebookConnectSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        透過 Facebook access token 建立 Facebook 帳號或是登入
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            access_token = serializer.data.get('access_token')
            try:
                st = SocialToken.objects.get(token=access_token)
                user = st.account.user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                if user.is_active:
                    login(request, user)

                serializer = UserInfoSerializer(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SocialToken.DoesNotExist:
                pass

            try:
                app = providers.registry.by_id(FacebookProvider.id).get_app(request)
                token = SocialToken(app=app, token=access_token)
                fb_login = fb_complete_login(request, app, token)

                complete_login(request, fb_login, app, token)
                serializer = UserInfoSerializer(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except requests.RequestException as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def complete_login(request, login, app, token):
    login.token = token
    login.state = SocialLogin.state_from_request(request)
    ret = complete_social_login(request, login)
    if not ret:
        ret = render_authentication_error(request)
