#-*- encoding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from action.models import Comment
from salmonella.admin import SalmonellaMixin

class CommentAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["user", "content", "date"]
    search_fields = ["user"]
    salmonella_fields  = ["user"]


admin.site.register(Comment, CommentAdmin)
