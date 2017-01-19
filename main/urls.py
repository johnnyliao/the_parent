
from django.conf.urls import patterns, url
from main.views import home, login, register, member

urlpatterns = patterns(".views",
	url("^$", home),
	url('^login/', login),
	url('^register/', register),
	url('^member/', member),

)
