from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def get_name(in_data):
	return in_data.extra_data["name"]

@register.filter
def get_fb_link(in_data):
	return "https://www.facebook.com/" + in_data.extra_data["id"]