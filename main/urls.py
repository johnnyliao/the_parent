
from django.conf.urls import patterns, url
from main.views import home, login, register, member, register_success

urlpatterns = patterns(".views",
	url("^$", home),
	url('^login/', login),
	url('^register/', register),
	url('^member/', member),
	url('^register_success/', register_success),

)
