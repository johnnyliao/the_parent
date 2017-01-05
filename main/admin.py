#-*- encoding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from main.models import S3Data


class S3DataAdmin(admin.ModelAdmin):
	list_display = ['key', 'bucket']


admin.site.register(S3Data, S3DataAdmin)