
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import patterns, include, url

from account.views import *

urlpatterns = format_suffix_patterns(patterns('',
	url('^facebook_connect/', FacebookConnectView.as_view()),
	url('^user_login/', UserLoginView.as_view()),
	url('^/social/signup/', social_login)),
	url('^user_logout/', UserLogoutView),
	url('^user_register/', UserRegisterView.as_view()),
	url('^user_modify/', UserModifyView.as_view()),
	(r'^', include('allauth.urls')),
	#url("^user_verify/$", UserVerifyView.as_view()),
	url("^user_verify/$", UserVerifyView),
	url("^re_send_verify/$", ReSendVerifyView),
	url("^check_user_verify/$", UserVerifyCheckView.as_view()),
	url("^user_change_password/$", UserChangePasswordView.as_view()),
	url("^user_forget_password/$", UserForgetPasswordView.as_view()),
))