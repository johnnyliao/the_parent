from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def get_name(in_data):
	return in_data.extra_data["name"]

@register.filter
def get_img(in_data):
	import pdb;pdb.set_trace()
	fb_id = in_data.extra_data["id"]
	pic_url = "http://graph.facebook.com/v2.8/%s/picture" % fb_id
	return pic_url
