from django import template
import datetime

register = template.Library()

@register.filter
def running_total(list_total):
  	return sum(d.group for d in list_total)

@register.filter
def week_report(list_data, start):
	today = datetime.date.today()
	list_data = list_data.filter(date__gte=start,date__lte=today).order_by("-date")[::-1]
	start_date = list_data[0]
	last_date = list_data[len(list_data) - 1]
	return last_date.hit_count - start_date.hit_count

@register.filter
def month_report(list_data, start):
	today = datetime.date.today()
	list_data = list_data.filter(date__gte=start,date__lte=today).order_by("-date")[::-1]
	start_date = list_data[0]
	last_date = list_data[len(list_data) - 1]
	return last_date.hit_count - start_date.hit_count
