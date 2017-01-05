#-*- encoding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from movie.models import Movie
from salmonella.admin import SalmonellaMixin

class MovieAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["title", "description", "movie_type"]
    search_fields = ["title"]
    list_filter  = ["movie_type"]


admin.site.register(Movie, MovieAdmin)
