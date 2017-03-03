#-*- encoding: utf-8 -*-

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from email.mime.text import MIMEText
from django.http import HttpResponse
import urllib, urllib2, json, simplejson

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.middleware.csrf import get_token
from movie.serializers import CommentLikeSerializer, CommentSerializer, ReCommentSerializer, VideoLikeSerializer
import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from movie.models import Comment, ReComment, Movie
from allauth.socialaccount.providers.twitter.provider import TwitterProvider
from allauth.socialaccount.providers.twitter.views import TwitterAPI

from allauth.socialaccount.providers.weibo.provider import WeiboProvider

from allauth.socialaccount.models import (SocialLogin, SocialToken, SocialAccount)
from allauth.socialaccount.helpers import complete_social_login, render_authentication_error

from django.contrib.auth import get_user_model
import smtplib
from django.contrib.auth import authenticate, login, logout
import settings, random
from rest_framework.views import APIView
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from datetime import datetime, timedelta
from django.db.models import Q
import pytz

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

class CommentLikeView(generics.GenericAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        留言按讚
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            comment_type = serializer.data.get('comment_type')
            comment_id = serializer.data.get('comment_id')
            if comment_type == "comment":
              comment = Comment.objects.get(id=comment_id)
              comment.like += 1
              comment.save()
            else:
              comment = ReComment.objects.get(id=comment_id)
              comment.like += 1
              comment.save()

            return Response(comment.like, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoLikeView(generics.GenericAPIView):
    serializer_class = VideoLikeSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        影片按讚
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            video_id = serializer.data.get('video_id')
            movie = Movie.objects.get(id=video_id)
            movie.like += 1
            movie.save()
            return Response(movie.like, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnVideoLikeView(generics.GenericAPIView):
    serializer_class = VideoLikeSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        影片取消按讚
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            video_id = serializer.data.get('video_id')
            movie = Movie.objects.get(id=video_id)
            movie.like -= 1
            movie.save()
            return Response(movie.like, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
