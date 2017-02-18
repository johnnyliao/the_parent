
from django.conf.urls import patterns, url
from fans.views import get_fans
urlpatterns = patterns(".views",

	url('^get_fans/', get_fans),

)
