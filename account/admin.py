#-*- encoding: utf-8 -*-
from django import forms

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
	list_display = ['username', 'nickname']


admin.site.register(User, UserAdmin)