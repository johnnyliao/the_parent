
from django.conf.urls import patterns, url
from main.views import home, login, register, member, register_success, forget_password, change_password, index, indexshop

urlpatterns = patterns(".views",
	url("^$", home),
	url('^login/', login),
	url('^register/', register),
	url('^member/', member),
	url('^index/', index),
	url('^indexshop/', indexshop),
	url('^register_success/', register_success),
	url('^forget_password/', forget_password),
	url('^change_password/', change_password),
)
