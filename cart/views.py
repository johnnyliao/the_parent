#-*- encoding: utf-8 -*-
from .cart import Cart
from .models import ProductInfo, FavoriteItem, PayMentRecord, PayMentInvoice, UserInvoice
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from .serializers import CartItemSerializer, FavoriteSerializer, CreateOrderSerializer
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
	serializer_class = CreateOrderSerializer
	permission_classes = (IsAuthenticated, )

	def post(self, request, format=None):
		"""
		結帳購物車內容
		"""
		serializer = self.serializer_class(data=request.DATA)
		if serializer.is_valid():
			item_arr = list()
			total_amount = 0
			item_name_arr = ""
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
				'ReturnURL':'http://nicokim.cc/cart/allpay_recevive/',
				'TotalAmount':total_amount,
				'TradeDesc':"111",
				'UnionPay':''
			}

			record = PayMentRecord(
				total_amount=total_amount,
				order_id=url_data["MerchantTradeNo"],
				user=request.user
			)

			record.save()
			for item in request.user.user_cart_item.all():
				#import pdb;pdb.set_trace()
				record.product.add(item.product)
				record.cart.add(item)

			record.save()

			szCheckMacValue = get_check_value(url_data)

			url_data["ItemName"] = item_name

			save_invoice_info(serializer.data, request.user, record)

			return Response({"CheckMacValue": szCheckMacValue, "url_data":url_data, "target":target})
		else:
			return Response(serializer.errors)

def save_invoice_info(invoice_data, user_id, record):
    user_invoice = UserInvoice.objects.filter(user=user_id)

    if user_invoice:
        user_invoice[0].customer_name = invoice_data["customer_name"]
        user_invoice[0].customer_addr = invoice_data["customer_addr"]
        user_invoice[0].customer_phone = invoice_data["customer_phone"]
        user_invoice[0].customer_email = invoice_data["customer_email"]

        # 非三聯式發票，就把統一編號清空
        if invoice_data["invoice_type"] == "3":
            user_invoice[0].customer_identifier=invoice_data["customer_identifier"]
        else:
            user_invoice[0].customer_identifier=""

        user_invoice[0].save()
    else:
        user_invoice = UserInvoice(
            customer_name=invoice_data["customer_name"],
            customer_addr=invoice_data["customer_addr"],
            customer_phone=invoice_data["customer_phone"],
            customer_email=invoice_data["customer_email"],
            user=user_id
        )

        if invoice_data["invoice_type"] == "3":
            user_invoice.customer_identifier = invoice_data["customer_identifier"]
        else:
            user_invoice.customer_identifier = ""

        user_invoice.save()

    # 捐贈才紀錄愛心碼
    if invoice_data["invoice_type"] == "1":
        donation = "1"
        love_code = invoice_data["love_code"]
    else:
        donation = "2"
        love_code = ""

    # 三聯式或二聯式紙本發票，要列印
    if invoice_data["invoice_type"] == "3" or (invoice_data["invoice_type"] == "2" and invoice_data["invoice_kind"] == "2"):
        print_type = "1"
    else:
        print_type = "0"

    # 沒有載具，載具資訊必須為空字串
    if invoice_data["carruer_type"] == "0" or invoice_data["carruer_type"] == "1":
        carruer_type = ""
        carruer_num = ""
    else:
        carruer_type = invoice_data["carruer_type"]
        carruer_num = invoice_data["carruer_num"]

    # 三聯式發票，一定是紙本
    if invoice_data["invoice_type"] == "3":
        invoice_kind = "2"
    else:
        invoice_kind = invoice_data["invoice_kind"]
    invoice = PayMentInvoice(
        invoice_type=invoice_data["invoice_type"],
        invoice_kind=invoice_kind,
        print_type=print_type,
        donation=donation,
        love_code=love_code,
        carruer_type=carruer_type,
        carruer_num=carruer_num,
        record=record,
    )

    invoice.save()
    print "save invoice"
    return "save invoice"

def create_invoice(order_id):
    payment_record = PayMentRecord.objects.filter(order_id=order_id)
    if not payment_record:
        return "can't find payment record"

    user_invoice = UserInvoice.objects.filter(user=payment_record[0].user_id)
    if not user_invoice:
        return "can't find user invoice"

    payment_invoice = PayMentInvoice.objects.filter(record_id=payment_record[0].id)
    if not payment_invoice:
        return "can't find payment invoice"

    if payment_invoice[0].donation == "1":
        love_code = payment_invoice[0].love_code
        print_type = "0"
    else:
        love_code = ""
        print_type = payment_invoice[0].print_type

    if print_type == "1":
        customer_identifier = user_invoice[0].customer_identifier
    else:
        customer_identifier = ""
    sales_amount = 0

    item_name_arr = list()
    item_count_arr = list()
    item_price_arr = list()
    item_amount_arr = list()
    item_word_arr = list()
    for cart in payment_record[0].cart.all():
    	item_name_arr.append(cart.product.item_name)
    	item_count_arr.append(cart.amount)
        item_price_arr.append(cart.product.total_amount)
        item_amount_arr.append(cart.product.total_amount * cart.amount)
    	item_word_arr.append(cart.product.unit)

	item_name = "| ".join('%s' % string for string in item_name_arr)
	item_count = "| ".join('%s' % string for string in item_count_arr)
    item_amount = "| ".join('%s' % string for string in item_amount_arr)
    item_price = "| ".join('%s' % string for string in item_price_arr)
    item_word = "| ".join('%s' % string for string in item_word_arr)


    url_data = {
        'TimeStamp': str(time.time()).split('.')[0],
        'RelateNumber': "ieachInvoice"+str(time.time()).replace(".",''),
        'MerchantID': "2000132",
        'CustomerID': "",
        'CustomerIdentifier': customer_identifier,
        'CustomerName': urllib.quote_plus(user_invoice[0].customer_name.encode("utf-8")),
        'CustomerAddr': urllib.quote_plus(user_invoice[0].customer_addr.encode("utf-8")),
        'CustomerPhone': "",
        'CustomerEmail': urllib.quote_plus(user_invoice[0].customer_email),
        'ClearanceMark': "",
        'Print': print_type,
        'Donation': payment_invoice[0].donation,
        'LoveCode': love_code,
        'CarruerType': payment_invoice[0].carruer_type,
        'CarruerNum': payment_invoice[0].carruer_num,
        'TaxType': "1",
        'SalesAmount': payment_record[0].total_amount,
        'ItemCount': item_count,
        'ItemPrice': item_price,
        'ItemAmount': item_amount,
        'InvType': "07",
        'ItemTaxType':"1|1|1",
    }

    url_data['CheckMacValue'] = get_invoice_check_value(url_data)
    url_data['ItemName'] = urllib.quote_plus(item_name.encode("utf-8"))
    url_data['ItemWord'] = urllib.quote_plus(item_word.encode("utf-8"))

    print url_data

    url_values = ''
    for k in sorted(url_data):
        #url_values += '&' + k + '=' + url_data[k]
        try:
            url_values += '&' + k + '='
            url_values += url_data[k]
        except TypeError:
            #數字需要轉換型態
            #import pdb;pdb.set_trace()
            url_values += str(url_data[k])

    #print url_values

    req = urllib2.Request('https://einvoice-stage.ecpay.com.tw/Invoice/Issue', url_values)
    response = urllib2.urlopen(req)
    the_page = response.read()
    rtn_data = dict(urlparse.parse_qsl(the_page, 1))

    receiveCheckMacValue = rtn_data['CheckMacValue']
    del rtn_data['CheckMacValue']
    verifyCheckMacValue = get_invoice_check_value(rtn_data)
    print "verifyCheckMacValue"
    print verifyCheckMacValue
    print "receiveCheckMacValue"
    print receiveCheckMacValue
    print "rtn_data['RtnCode'"
    print rtn_data['RtnCode']
    print rtn_data['RtnMsg']

    if verifyCheckMacValue == receiveCheckMacValue and rtn_data['RtnCode'] == '1':
        payment_invoice[0].relate_number = url_data['RelateNumber']
        payment_invoice[0].tax_type = url_data['TaxType']
        payment_invoice[0].inv_type = url_data['InvType']
        payment_invoice[0].random_number = rtn_data['RandomNumber']
        payment_invoice[0].invoice_date = rtn_data['InvoiceDate']
        payment_invoice[0].invoice_number = rtn_data['InvoiceNumber']
        payment_invoice[0].invoice_rtn_msg = rtn_data['RtnMsg']
        payment_invoice[0].save()

        return "create invoice success"

    print "create invoice fail"
    return "create invoice fail"

def get_invoice_check_value(url_data):
    hashkey = "ejCk326UnaZWKisg"
    HashIV = "q9jcZX8Ib9LM8wYk"

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

    check_value = check_value.replace("+",' ')
    url_encode = urllib.quote_plus(check_value)
    url_encode = url_encode.lower()

    m = hashlib.md5(url_encode)
    md5 = m.hexdigest()
    check =  md5.upper()
    return check

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
    def get(self, request, format=None):
        print request.POST
        print request.GET
        return Response("1|OK")

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
            return Response("0|check mac value error")

        else:
            print "check mac value OK"
            #try:
            record = PayMentRecord.objects.filter(order_id=post_data['MerchantTradeNo'])
            if record:
                print "have record"
                record = record[0]
                if record.is_checked:
                    return Response("0|record was checked")
                else:
                    record.is_checked = True
                    record.save()

                    create_invoice(post_data['MerchantTradeNo'])
                    print "1|OK"
                    return Response("1|OK")
            else:
                return Response("0|no record")

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
