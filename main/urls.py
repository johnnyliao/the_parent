
from django.conf.urls import patterns, url
from main.views import home, login, register, member, register_success, forget_password, change_password, index, indexshop, product_detail, now_cart, cart_check, cart_final, pay_success, action, auto_reply, index_video, videoDetails, index_home

urlpatterns = patterns(".views",
	url("^$", home),
	#url('^login/', login),
	#url('^register/', register),
	#url('^member/', member),
	#url('^index/', index),
	#url('^pay_success/', pay_success),
	#url('^now_cart/', now_cart),
	#url('^indexshop/', indexshop),
	#url('^cart_check/', cart_check),
	#url('^cart_final/', cart_final),
	url('^action/', action),
	url('^index_video/', index_video),
	url('^videoDetails/', videoDetails),
	url('^auto_reply/', auto_reply),
	url('^home/', index_home),
	#url('^register_success/', register_success),
	#url('^forget_password/', forget_password),
	#url('^change_password/', change_password),
	#url('^product_detail/(?P<pk>\d+)/$', product_detail),
)
