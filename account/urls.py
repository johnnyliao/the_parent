
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import patterns, include, url

from account.views import *

urlpatterns = format_suffix_patterns(patterns('',
	url('^facebook_connect/', FacebookConnectView.as_view()),
	url('^user_login/', UserLoginView.as_view()),
	url('^user_register/', UserRegisterView.as_view()),
	(r'^', include('allauth.urls')),
	#url("^user_verify/$", UserVerifyView.as_view()),
	url("^user_verify/$", UserVerifyView),
	url("^check_user_verify/$", UserVerifyCheckView.as_view()),
))