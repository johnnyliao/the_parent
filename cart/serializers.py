#-*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from .models import ProductInfo, CartItem, FavoriteItem

from rest_framework import serializers

from datetime import datetime,timedelta
from django.utils import timezone
import urlparse
from django.contrib.sites.models import Site

class ProductInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = ProductInfo

class CartItemSerializer(serializers.ModelSerializer):
	product = ProductInfoSerializer()
	class Meta:
		model = CartItem


class FavoriteSerializer(serializers.ModelSerializer):
	product = ProductInfoSerializer()
	class Meta:
		model = FavoriteItem

class CreateOrderSerializer(serializers.Serializer):
    invoice_type = serializers.CharField()
    invoice_kind = serializers.CharField()
    carruer_type = serializers.CharField(blank=True)
    carruer_num = serializers.CharField(blank=True)
    love_code = serializers.CharField(blank=True)
    customer_identifier = serializers.CharField(blank=True)
    customer_name = serializers.CharField(blank=True)
    customer_addr = serializers.CharField(blank=True)
    customer_phone = serializers.CharField()
    customer_email = serializers.CharField()
