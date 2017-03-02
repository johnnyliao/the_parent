#-*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from account.models import *
from salmonella.admin import SalmonellaMixin

class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User

class UserCreationForm(DjangoUserCreationForm):
	class Meta:
		model = User
		fields = ('username', )

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User._default_manager.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['duplicate_username'])

class UserAdmin(SalmonellaMixin, DjangoUserAdmin):
	add_form = UserCreationForm
	form = UserChangeForm
	list_display = ['username', 'nickname', 'image_tag']

def send_to_all_user(modeladmin, request, queryset):
	for obj in User.objects.all():
		user_msg = UserMsg.objects.create(user=obj, msg=queryset[0])


send_to_all_user.short_description = _(u"發送給所有使用者")


class MessageAdmin(admin.ModelAdmin):
	list_display = ["title"]
	actions = [send_to_all_user]

class WinningDataAdmin(admin.ModelAdmin):
	list_display = ["name", "prize", "phone", "address", "is_check"]

class UserMsgAdmin(admin.ModelAdmin):
	list_display = ["user", "is_read", "time"]

admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserMsg, UserMsgAdmin)
admin.site.register(WinningData, WinningDataAdmin)