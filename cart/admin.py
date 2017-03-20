#-*- encoding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from .models import CartItem, ProductInfo, PayMentRecord, PayMentInvoice, ProductImage, Brand, BrandBanner, BrandMovie
from salmonella.admin import SalmonellaMixin

class CartItemAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["user", "creation_date", "is_checked_out", "amount"]
    search_fields = ["user", "creation_date", "is_checked_out", "amount"]
    #salmonella_fields  = ["user", "product"]

class ProductImageAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["image_tag"]
    #salmonella_fields  = ["user", "product"]


class ProductInfoAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["item_name", "total_amount", "date", "unit"]
    salmonella_fields  = ["photo", "brand"]

class PayMentInvoiceAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["relate_number", "invoice_number", "invoice_type", "invoice_kind", "print_type", "love_code", "carruer_type", "carruer_num", "invoice_rtn_msg", "invoice_date", "invalid_reason", "invalid_rtn_msg", "invalid_time"]

class PayMentInvoiceInline(admin.StackedInline):
    model = PayMentInvoice

class PayMentRecordAdmin(SalmonellaMixin, admin.ModelAdmin):
    inlines = (PayMentInvoiceInline,)
    list_display = ["order_id", "total_amount", "user", "is_checked", "date"]
    salmonella_fields  = ["product", "cart", "user"]
    search_fields = ['order_id']
    list_filter = ["is_checked"]

class BrandAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["brand_name"]
    salmonella_fields  = ["banner", "movie"]

class BrandBannerAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["name", "image_tag"]

class BrandMovieAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ["name", "link"]

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(PayMentInvoice, PayMentInvoiceAdmin)
admin.site.register(PayMentRecord, PayMentRecordAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(BrandBanner, BrandBannerAdmin)
admin.site.register(BrandMovie, BrandMovieAdmin)