from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def get_name(in_data):
	return in_data.extra_data["name"]

@register.filter
def get_fb_link(in_data):
	return "https://www.facebook.com/" + in_data.extra_data["id"]

@register.filter
def get_user_img(in_data):
	if in_data.socialaccount_set.all():
		fb_id = in_data.socialaccount_set.all()[0].extra_data["id"]
		pic_url = "http://graph.facebook.com/v2.8/%s/picture" % fb_id
		return pic_url
	else:
		return "/static/img/person-icon.png"

@register.filter
def split_videos(in_data):
	total = in_data.count()
	result = []
	start = 0
	range_num = 5
	while start < total:
		result.append(in_data[start:start+range_num])
		start = start + range_num

	return result