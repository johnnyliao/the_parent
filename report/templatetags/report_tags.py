from django import template
import datetime

register = template.Library()

@register.filter
def running_total(list_total):
  	return sum(d.group for d in list_total)

@register.filter
def week_report(list_data, start):
	if list_data.every_day_data.all().count():
		today = datetime.date.today()
		list_data = list_data.every_day_data.all().filter(date__gte=start,date__lte=today).order_by("-date")[::-1]
		if list_data.date >= start and list_data.date <= today:
			start_count = list_data.base_count
		else:
			start_count = list_data[0].hit_count
		last_date = list_data[len(list_data) - 1]
		return last_date.hit_count - start_count
	else:
		return ""

@register.filter
def month_report(list_data, start):
	if list_data.every_day_data.all().count():
		today = datetime.date.today()
		list_data = list_data.every_day_data.all().filter(date__gte=start,date__lte=today).order_by("-date")[::-1]
		if list_data.date >= start and list_data.date <= today:
			start_count = list_data.base_count
		else:
			start_count = list_data[0].hit_count
		last_date = list_data[len(list_data) - 1]
		return last_date.hit_count - start_count
	else:
		return ""
