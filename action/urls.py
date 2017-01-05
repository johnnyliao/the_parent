
from django.conf.urls import patterns, url
from action.views import comment
urlpatterns = patterns(".views",

	url('^comment/', comment),
)
