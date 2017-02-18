#-*- encoding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from movie.models import Movie, Comment, ReComment
from salmonella.admin import SalmonellaMixin

class MovieAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["image_tag", "title", "movie_type"]
    search_fields = ["title"]
    list_filter  = ["movie_type"]

class CommentAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["user", "content", "date"]
    search_fields = ["user"]
    salmonella_fields  = ["user", "movie"]

class ReCommentAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["user", "content", "date"]
    search_fields = ["user"]
    salmonella_fields  = ["user", "re_comment"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(ReComment, ReCommentAdmin)
admin.site.register(Comment, CommentAdmin)
