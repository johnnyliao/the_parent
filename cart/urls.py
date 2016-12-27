
from django.conf.urls import patterns, url
from .views import add_to_cart, remove_cart, get_cart, update_cart

urlpatterns = patterns(".views",

   	url('^add_cart/', add_to_cart.as_view()),
   	url('^update_cart/', update_cart.as_view()),
   	url('^remove_cart/', remove_cart.as_view()),
   	url('^get_cart/', get_cart.as_view()),
)
