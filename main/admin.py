#-*- encoding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from main.models import S3Data, BrandIndex, BrandIndexBanner, BrandIndexMovie
from salmonella.admin import SalmonellaMixin

class S3DataAdmin(admin.ModelAdmin):
	list_display = ['key', 'bucket']

class BrandIndexAdmin(SalmonellaMixin, admin.ModelAdmin):
    #list_display = ["brand_name"]
    salmonella_fields  = ["banner", "movie", "brand"]

class BrandIndexBannerAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["name", "image_tag"]

class BrandIndexMovieAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["name", "link"]

#admin.site.register(S3Data, S3DataAdmin)
admin.site.register(BrandIndex, BrandIndexAdmin)
admin.site.register(BrandIndexBanner, BrandIndexBannerAdmin)
admin.site.register(BrandIndexMovie, BrandIndexMovieAdmin)
