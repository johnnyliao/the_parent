
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import patterns, include, url

from account.views import *

urlpatterns = format_suffix_patterns(patterns('',
	url('^facebook_connect/', FacebookConnectView.as_view()),
))