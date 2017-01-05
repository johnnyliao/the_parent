#-*- encoding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from .models import CartItem, ProductInfo, PayMentRecord, PayMentInvoice, ProductImage
from salmonella.admin import SalmonellaMixin

class CartItemAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["user", "creation_date", "is_checked_out", "amount"]
    search_fields = ["user", "creation_date", "is_checked_out", "amount"]
    #salmonella_fields  = ["user", "product"]

class ProductImageAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["image_tag"]
    #salmonella_fields  = ["user", "product"]


class ProductInfoAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["item_name", "total_amount", "trade_desc", "date"]
    salmonella_fields  = ["photo"]

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
