#-*- encoding: utf-8 -*-
from .cart import Cart
from .models import ProductInfo
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from .serializers import CartItemSerializer

class add_to_cart(APIView):
	#serializer_class = PasswordResetSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		"""
        加入購物車
        product_id -- 商品ID
        quantity -- 數量
        """
		product_id = request.QUERY_PARAMS.get('product_id')
		quantity = request.QUERY_PARAMS.get('quantity')
		product = ProductInfo.objects.get(id=product_id)
		cart = Cart()
		cart.add(product, request, int(quantity))
		serializer = CartItemSerializer(request.user.user_cart_item.all(), many=True)
		return Response(serializer.data)

class remove_cart(APIView):
	#serializer_class = PasswordResetSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		"""
        刪除購物車商品
        product_id -- 商品ID
        """
		product_id = request.QUERY_PARAMS.get('product_id')
		product = ProductInfo.objects.get(id=product_id)
		cart = Cart()
		status = cart.remove(product, request)
		serializer = CartItemSerializer(request.user.user_cart_item.all(), many=True)
		return Response(serializer.data)

class update_cart(APIView):
	#serializer_class = PasswordResetSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		"""
        更新購物車商品數量
        product_id -- 商品ID
        quantity -- 數量
        """
		product_id = request.GET.get("product_id")
		quantity = request.GET.get("quantity")
		product = ProductInfo.objects.get(id=product_id)
		cart = Cart()
		status = cart.update(product, request, quantity)
		serializer = CartItemSerializer(request.user.user_cart_item.all(), many=True)
		return Response(serializer.data)

class get_cart(APIView):
	#serializer_class = PasswordResetSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		print request.user.user_cart_item.all()
		return Response("OK")