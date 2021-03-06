from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def running_total(list_total):
  	return sum(d.group for d in list_total)

@register.filter
def week_report(list_data, start):
	if list_data.every_day_data.all().count():
		today = datetime.date.today()
		list_datas = list_data.every_day_data.all().filter(date__gte=start,date__lte=today).order_by("-date")[::-1]
		if list_data.date.date() >= start and list_data.date.date() <= today:
			start_count = list_data.base_count
		else:
			start_count = list_datas[0].hit_count
		last_date = list_datas[len(list_datas) - 1]
		return last_date.hit_count - start_count
	else:
		return ""

@register.filter
def month_report(list_data, start):
	if list_data.every_day_data.all().count():
		today = datetime.date.today()
		list_datas = list_data.every_day_data.all().filter(date__gte=start,date__lte=today).order_by("-date")[::-1]

		#import pdb;pdb.set_trace()
		if list_data.date.date() >= start and list_data.date.date() <= today:
			start_count = list_data.base_count
		else:
			start_count = list_datas[0].hit_count
		last_date = list_datas[len(list_datas) - 1]
		return last_date.hit_count - start_count
	else:
		return ""

@register.filter
def get_list_first(list_data, start):
	if list_data.every_day_data.all().count():
		today = datetime.date.today()
		list_datas = list_data.every_day_data.all().filter(date__gte=start,date__lte=today).order_by("-date")[::-1]
		return list_datas[0].date
	else:
		return ""

@register.filter
def get_list_last(list_data, start):
	if list_data.every_day_data.all().count():
		today = datetime.date.today()
		list_datas = list_data.every_day_data.all().filter(date__gte=start,date__lte=today).order_by("-date")[::-1]
		return list_datas[len(list_datas) - 1].date
	else:
		return ""

@register.filter
def get_week_total(date, list_data):
	#import pdb;pdb.set_trace()
	sum_data = list_data.filter(date=date).aggregate(Sum("group"))
	if not sum_data["group__sum"]:
		return 0
	else:
		return sum_data["group__sum"]
