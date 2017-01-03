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


