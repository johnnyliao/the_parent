
from django.conf.urls import patterns, url
from fans.views import get_fans, fans_report, group_up
urlpatterns = patterns(".views",

	url('^get_fans/', get_fans),
	url('^report/', fans_report),
	url('^group_up/', group_up),

)
