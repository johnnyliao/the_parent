#-*- encoding: utf-8 -*-

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required
from account.models import User, UserVerify
from account.serializers import FacebookConnectSerializer, UserInfoSerializer, UserLoginSerializer, UserRegisterSerializer, UserChangePasswordSerializer, UserModifySerializer, UserForgetPasswordSerializer
from django.http import HttpResponse
import urllib, urllib2, json, simplejson

from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.middleware.csrf import get_token
from account import sms
import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from allauth.socialaccount.providers.facebook.views import fb_complete_login

from allauth.socialaccount.providers.twitter.provider import TwitterProvider
from allauth.socialaccount.providers.twitter.views import TwitterAPI
import smtplib
from email.mime.text import MIMEText
from allauth.socialaccount.providers.weibo.provider import WeiboProvider

from allauth.socialaccount.models import (SocialLogin, SocialToken, SocialAccount)
from allauth.socialaccount.helpers import complete_social_login, render_authentication_error

from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, login, logout
import settings, random
from django.contrib import auth
from rest_framework.views import APIView
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from datetime import datetime, timedelta
from django.db.models import Q
from main.views import login as login_view
from main.views import member
import pytz

def social_login(request):
    if not request.user.is_verified:
        print "create verify"
        verify = UserVerify.objects.create(user=request.user, date_verified=datetime.now())
    return redirect(member)

def UserLogoutView(request):
    auth.logout(request)
    return redirect(login_view)

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
                User.objects.get(username=username)
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        #import pdb;pdb.set_trace()
                        login(request, user)
                else:
                    return Response({"status":False, "msg":u"錯誤的帳號或密碼"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"status":False, "msg":u"使用者帳號錯誤"}, status=status.HTTP_200_OK)

            serializer = UserInfoSerializer(request.user, context={'request': request})
            return Response({"status":True}, status=status.HTTP_201_CREATED)
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
            nickname = serializer.data.get('nickname')
            password = serializer.data.get('password')
            #re_password = serializer.data.get('re_password')
            phone_number = serializer.data.get('phone_number')
            year = serializer.data.get('year')
            sex = serializer.data.get('sex')
            address = serializer.data.get('address')
            birthday = serializer.data.get('birthday')
            city = serializer.data.get('city')
            district = serializer.data.get('district')
            try:
                user = User.objects.get(username=username)
                return Response({"status":False, "msg":u"此帳號以註冊過！"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                        username=username,
                        password=password,
                        nickname=nickname,
                        phone_number=phone_number,
                        year=year,
                        sex=sex,
                        email=username,
                        address=address,
                        birthday=birthday,
                        city=city,
                        district=district,
                    )
                user.set_password(password)
                user.save()
                user.backend = 'mezzanine.core.auth_backends.MezzanineBackend'
                login(request, user)
                #UserVerify.objects.create(user=user)
            serializer = UserInfoSerializer(user)
            return Response({"status":True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":False, "msg":serializer.errors}, status=status.HTTP_200_OK)

class UserModifyView(generics.GenericAPIView):
    serializer_class = UserModifySerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        註冊網站帳號或修改帳號資訊
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():

            username = serializer.data.get('username')
            nickname = serializer.data.get('nickname')
            phone_number = serializer.data.get('phone_number')
            year = serializer.data.get('year')
            sex = serializer.data.get('sex')
            address = serializer.data.get('address')
            birthday = serializer.data.get('birthday')
            city = serializer.data.get('city')
            district = serializer.data.get('district')
            email = serializer.data.get("email", None)
            try:
                user = User.objects.get(username=username)
                user.nickname = nickname
                user.phone_number = phone_number
                user.year = year
                user.sex = sex
                user.city = city
                user.district = district
                user.email = username
                user.address = address
                user.birthday = birthday
                print user.email
                print email
                if email:
                    #import pdb;pdb.set_trace()
                    if user.email != email:
                        user.email = email
                        #只有fb帳號可改email
                        redirect = True
                    else:
                        redirect = False
                user.save()
            except User.DoesNotExist:
                return Response({"status":False, "msg":u"使用者帳號錯誤"}, status=status.HTTP_200_OK)

            serializer = UserInfoSerializer(user)
            if redirect:
                return Response({"status":True, "redirect":True}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":True, "redirect":False}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":False, "msg":serializer.errors}, status=status.HTTP_200_OK)


class UserChangePasswordView(generics.GenericAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        使用者修改密碼
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_password')
            if request.user.check_password(old_password):
                if new_password == confirm_password:
                    request.user.set_password(confirm_password)
                    request.user.save()
                    return Response({"status":True}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":False, "msg":u"密碼輸入不相同！"}, status=status.HTTP_200_OK)
            else:
                return Response({"status":False, "msg":u"密碼錯誤！"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserForgetPasswordView(generics.GenericAPIView):
    serializer_class = UserForgetPasswordSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        使用者忘記密碼
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            username = serializer.data.get('username')
            try:
                user = User.objects.get(username=username)
                verify_code = sms.generate_verify_code()
                new_password = "nicokim" + str(verify_code)
                user.set_password(new_password)
                user.save()
                try:
                    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp_obj.starttls()
                    smtp_obj.login("web@supermedia.cool","ttshow321")
                    domain_name = Site.objects.get_current().domain
                    html_text = u"請使用新密碼登入後再修改密碼！<br/><br/>新密碼為"+new_password+u"<br/><br/<a href="+domain_name.encode('utf-8')+u"main/login/>登入那對夫妻</a><br/><br/>"
                    msg = MIMEText(html_text,_subtype='html',_charset='utf8')
                    msg['Subject'] = '那對夫妻忘記密碼'
                    me = '超人氣娛樂<web@supermedia.cool>'
                    msg['From'] = me
                    msg['To'] = user.email
                    smtp_obj.sendmail(me,user.email,msg.as_string())
                    print "send verify email "

                    smtp_obj.close()

                    return Response({"status":True}, status=status.HTTP_200_OK)

                except Exception, e:
                    self.is_send = False
                    self.errors = e.args
                    return Response({"status":False, "msg":u"寄送忘記密碼失敗！"}, status=status.HTTP_200_OK)

            except:
                return Response({"status":False, "msg":u"錯誤的使用者名稱！"}, status=status.HTTP_200_OK)

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

class UserVerifyCheckView(APIView):
    #serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        """
        確認使用者email認證狀態

        """

        return Response(request.user.is_verified())

def UserVerifyView(request):
    #serializer_class = PasswordResetSerializer
    #permission_classes = (IsAuthenticated, )

    #def get(self, request, format=None):
    """
    認證使用者email
    code -- code
    """
    #import pdb;pdb.set_trace()
    code = request.GET.get('code')
    account = request.GET.get('account')
    if account and code:
        try:
            user = User.objects.get(username=account)
        except:
            msg = u"查無使用者帳號！"
            return render_to_response("main/VerFailure.html", locals(), context_instance=RequestContext(request))

        try:
            verify_valid = user.verify.is_verify_code_valid(code)
            print verify_valid
        except:
            verify_valid = "over_date"
            msg = u"認證失敗！認證碼已過期，請重新認證！"
            return render_to_response("main/VerFailure.html", locals(), context_instance=RequestContext(request))
        return render_to_response("main/VerSuccess.html", locals(), context_instance=RequestContext(request))

@login_required
def ReSendVerifyView(request):
    #serializer_class = PasswordResetSerializer
    #permission_classes = (IsAuthenticated, )

    #def get(self, request, format=None):
    """
    重發認證使用者email
    """
    #import pdb;pdb.set_trace()
    request.user.verify.resend_verify_code()

    return HttpResponse("ok", status=status.HTTP_200_OK)


