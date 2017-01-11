
from django.conf.urls import patterns, url
from main.views import home, login, index, index1, album, inner, photo, video, add_to_cart, filter_list, ui_inner, register

urlpatterns = patterns(".views",
	url("^$", home),
	url("^index/", index),
	url("^index1/", index1),
	url('^login/', login),
	url('^album/', album),
	url('^inner/', inner),
	url('^photo/', photo),
	url('^video/', video),
	url('^add_to_cart/', add_to_cart),
	url('^filter_list/', filter_list),
	url('^ui_inner/', ui_inner),
	url('^register/', register),

)
