#-*- encoding: utf-8 -*-
from .models import ProductInfo, CartItem
from django.core.exceptions import ObjectDoesNotExist

class Cart:
    def add(self, product, request, quantity=1):
        try:
            cart_item = request.user.user_cart_item.all().get(product=product)
            cart_item.amount += quantity

        except ObjectDoesNotExist:
            cart_item = CartItem()
            cart_item.user = request.user
            cart_item.product = product
            cart_item.amount = quantity
            cart_item.quantity = quantity
            cart_item.quantity = quantity
            cart_item.quantity = quantity

        cart_item.save()

    def remove(self, product, request):
        try:
            cart_item = request.user.user_cart_item.all().get(product=product)
            cart_item.is_checked = True
            cart_item.save()
            return True

        except ObjectDoesNotExist:
            return False

    def update(self, product, request, quantity):
        try:
            cart_item = request.user.user_cart_item.all().get(product=product)
            cart_item.amount = quantity
            cart_item.save()
            return True
        except ObjectDoesNotExist:
            return False


    def clear(self):
        pass

