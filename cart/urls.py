
from django.conf.urls import patterns, url
from .views import add_to_cart, remove_cart, get_cart, update_cart, remove_favorite, add_favorite, get_favorite

urlpatterns = patterns(".views",

   	url('^add_cart/', add_to_cart.as_view()),
   	url('^update_cart/', update_cart.as_view()),
   	url('^remove_cart/', remove_cart.as_view()),
   	url('^remove_favorite/', remove_favorite.as_view()),
   	url('^get_cart/', get_cart.as_view()),
   	url('^get_favorite/', get_favorite.as_view()),
   	url('^add_favorite/', add_favorite.as_view()),
)
