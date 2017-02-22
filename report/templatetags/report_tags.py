from django import template

register = template.Library()

@register.filter
def running_total(list_total):
  	return sum(d.group for d in list_total)