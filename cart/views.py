#-*- encoding: utf-8 -*-
from .cart import Cart
from .models import ProductInfo, FavoriteItem
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from .serializers import CartItemSerializer, FavoriteSerializer
from rest_framework import generics, status
import json, requests, urllib, urllib2, re, base64, os, datetime
import urlparse, time, cookielib, hashlib, time
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

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

class cart_check_out(APIView):
	#serializer_class = PasswordResetSerializer
	permission_classes = (IsAuthenticated, )

	def get(self, request, format=None):
		"""
		結帳購物車內容
		"""
		item_arr = list()
		total_amount = 0
		for name in request.user.user_cart_item.all():
			#import pdb;pdb.set_trace()
			item_arr.append(name.product.item_name)
			total_amount += (name.product.total_amount * name.amount)
			item_name = ",".join(item_arr)
			item_name_arr = "#".join(item_arr)

		target = "_self"
		ServiceURL = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V2"
		url_data = {
			'ChoosePayment':"ALL",
			'ChooseSubPayment':'',
			'ClientBackURL':'http://www.dodohouse.com.tw/',
			'CreditInstallment':'0',
			'DeviceSource':'',
			'EncryptType':'0',
			'ExecTimes':'',
			'Frequency':'',
			'InstallmentAmount':'0',
			'InvoiceMark':'',
			'ItemName':item_name_arr,
			'ItemURL':'dedwed ',
			'Language':'',
			'MerchantID':'2000132',
			'MerchantTradeDate':datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S'),
			'MerchantTradeNo':"Test"+  str(time.time()).replace(".",''),
			'NeedExtraPaidInfo':'N',
			'OrderResultURL':'',
			'PaymentType':'aio',
			'PeriodAmount':'',
			'PeriodReturnURL':'',
			'PeriodType':'',
			'Redeem':'',
			'Remark':'',
			'ReturnURL':'http://app.i-each.com.tw/account/allpay_recevive/',
			'TotalAmount':total_amount,
			'TradeDesc':"111",
			'UnionPay':''
		}

		szCheckMacValue = get_check_value(url_data)

		url_data["ItemName"] = item_name

		return Response({"CheckMacValue": szCheckMacValue, "url_data":url_data, "target":target})


def get_check_value(url_data):
    hashkey = "5294y06JbISpM5x9"
    HashIV = "v77hoKGq4kWxNNIS"

    check_value = 'HashKey=' + hashkey
    for k in sorted(url_data):
        try:
            check_value += '&' + k + '='
            check_value += url_data[k]
        except TypeError:
            #數字需要轉換型態
            #import pdb;pdb.set_trace()
            check_value += str(url_data[k])

    check_value += '&HashIV=' + HashIV
    url_encode =  urllib.quote_plus(check_value.encode("utf-8"))
    print "\n\n\n\n"
    print url_encode
    m = hashlib.md5(url_encode.lower())
    md5 = m.hexdigest()
    check =  md5.upper()

    print check
    #import pdb;pdb.set_trace()
    return check

class allpay_recevive(APIView):
    #serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        post_data = request.POST.copy()
        CheckMacValue = post_data["CheckMacValue"]
        del post_data['CheckMacValue']
        HashKey = "5294y06JbISpM5x9"
        HashIV = "v77hoKGq4kWxNNIS"
        #check_value = 'HashKey=' + hashkey

        check_value = ""
        check_value = "HashKey=5294y06JbISpM5x9"
        for k in sorted(post_data):
            check_value += "&" + k + "=" +post_data[k]
        check_value += '&HashIV=' + HashIV
        check_value = urllib.quote_plus(check_value.encode("utf-8"))
        print check_value
        m = hashlib.md5(check_value.lower())
        md5 = m.hexdigest()
        check =  md5.upper()
        if CheckMacValue != check:
            print "\n\n\n\n"
            print "check mac value error"
            return Response("OK")

        else:
            print "check mac value OK"
            return Response("OK")

def order_create(request):
    product_info = ProductInfo.objects.all()
    user_id = request.user.id
    print "\n\n\n"
    print user_id
    return render_to_response("account/create_order.html", locals(), context_instance=RequestContext(request))

def receive_order(request):
    ServiceURL = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V2"

    CheckMacValue = request.GET.get("CheckMacValue")
    #import pdb;pdb.set_trace()
    url_data = json.loads(request.GET.get("url_data"), encoding="utf-8")
    url_data["ItemName"] = url_data["ItemName"].replace(",", "#")
    url_data = convert_url_data(url_data)
    #CheckMacValue = get_check_value(url_data)
    target = "_self"
    print CheckMacValue
    print "\n\n\n\n"
    print url_data
    #import pdb;pdb.set_trace()
    return render_to_response("cart/point.html", locals())

def convert_url_data(url_data):
    return_data = {}
    for key in url_data:
        if key != "ItemName" and key != "TotalAmount":
            try:
                return_data.update({key:url_data[key].encode("utf-8")})
            except:
                import pdb;pdb.set_trace()
        else:
            return_data.update({key:url_data[key]})
    return return_data

def check_out_cart(request):
    return render_to_response("cart/check_out.html", locals(), context_instance=RequestContext(request))
