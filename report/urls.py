
from django.conf.urls import patterns, url
from report.views import *
urlpatterns = patterns(".views",

	url('^add/', register),
	url('^login/', login),
	url('^add_inner/', AddInner.as_view()),
	url('^day_record/', day_record),
	url('^day_group_up/', day_group_up),
	url('^report/', group_report),
	url('^get_report/', get_report),
)
