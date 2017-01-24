
from django.conf.urls import patterns, url
from main.views import home, login, register, member, register_success, forget_password, change_password, index, indexshop, product_detail, now_cart, cart_check, cart_final

urlpatterns = patterns(".views",
	url("^$", index),
	url('^login/', login),
	url('^register/', register),
	url('^member/', member),
	url('^index/', index),
	url('^now_cart/', now_cart),
	url('^indexshop/', indexshop),
	url('^cart_check/', cart_check),
	url('^cart_final/', cart_final),
	url('^register_success/', register_success),
	url('^forget_password/', forget_password),
	url('^change_password/', change_password),
	url('^product_detail/(?P<pk>\d+)/$', product_detail),
)
