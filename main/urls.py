
from django.conf.urls import patterns, url
from main.views import home

urlpatterns = patterns(".views",
	url("^$", home),

)
