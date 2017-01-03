#-*- encoding: utf-8 -*-
from .cart import Cart
from .models import ProductInfo, FavoriteItem
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from .serializers import CartItemSerializer, FavoriteSerializer

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

class add_favorite(APIView):
	#serializer_class = PasswordResetSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		"""
        加入最愛
        product_id -- 商品ID
        """
		product_id = request.QUERY_PARAMS.get('product_id')
		product = ProductInfo.objects.get(id=product_id)
		try:
			favorite = FavoriteItem.objects.get(product=product, user=request.user)
		except:
			favorite = FavoriteItem(product=product, user=request.user)
			favorite.save()
		serializer = FavoriteSerializer(request.user.user_favorite_item.all(), many=True)
		return Response(serializer.data)

class remove_favorite(APIView):
	#serializer_class = PasswordResetSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		"""
        刪除最愛商品
        product_id -- 商品ID
        """
		product_id = request.QUERY_PARAMS.get('product_id')
		product = ProductInfo.objects.get(id=product_id)
		try:
			favorite = FavoriteItem.objects.get(product=product, user=request.user)
			favorite.delete()
		except:
			pass

		serializer = FavoriteSerializer(request.user.user_favorite_item.all(), many=True)
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
	serializer_class = CartItemSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		user_cart = request.user.user_cart_item.all()
		if user_cart:
			serializer = CartItemSerializer(user_cart, many=True)
			return Response(serializer.data)
		else:
			return Response({})

class get_favorite(APIView):
	serializer_class = CartItemSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		user_favorite = request.user.user_favorite_item.all()
		if user_favorite:
			serializer = FavoriteSerializer(user_favorite, many=True)
			return Response(serializer.data)
		else:
			return Response({})