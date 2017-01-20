#-*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from account.models import User
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

from django.contrib.contenttypes import generic

from django.core.exceptions import ObjectDoesNotExist
from mezzanine.core.fields import RichTextField
from django.contrib.sites.models import Site
import urlparse, settings

INVOICE_TYPE_CHOICES = (
    ("1", _(u'捐贈')),
    ("2", _(u'二聯式')),
    ("3", _(u'三聯式')),
)

INVOICE_KIND_CHOICES = (
    (0, _(u'無')),
    (1, _(u'電子')),
    (2, _(u'紙本')),
)

CARRUER_TYPE_CHOICES = (
    ("", _(u'沒有載具')),
    ("2", _(u'自然人憑證')),
    ("3", _(u'手機條碼')),
)

PRINT_TYPE_CHOICES = (
    ("0", _(u'否')),
    ("1", _(u'是')),
)

DONATION_CHOICES = (
    ("1", _(u'捐贈')),
    ("2", _(u'不捐贈')),
)

class UserInvoice(models.Model):
    customer_identifier = models.CharField(_(u"統一編號"), max_length=8, null=True, blank=True)
    customer_name = models.CharField(_(u"客戶名稱"), max_length=20, null=True, blank=True)
    customer_addr = models.CharField(_(u"客戶地址"), max_length=100, null=True, blank=True)
    customer_phone = models.CharField(_(u"客戶手機號碼"), max_length=20, null=True, blank=True)
    customer_email = models.CharField(_(u"客戶電子信箱"), max_length=80, null=True, blank=True)
    user = models.OneToOneField(User,  related_name='user_invoice')


class ProductImage(models.Model):
    photo = models.ImageField(_(u"商品照片"), upload_to='cart/productinfo')

    def image_tag(self):
        return '<img style="width:100px;height:100px" src="' + self.photo.url + '" />'

    image_tag.allow_tags = True

class ProductInfo(models.Model):
    total_amount = models.IntegerField(_(u"金額"))
    trade_desc = RichTextField(_(u"商品描述"), max_length=2000)
    item_name = models.CharField(_(u"商品名稱"), max_length=30)
    date = models.DateTimeField(_(u"建立時間"), auto_now=True)
    photo = models.ManyToManyField("ProductImage", verbose_name=_(u"商品照片"), related_name='product_images')
    #photo = models.CharField(_(u"商品圖片"), max_length=50)
    video_link = models.CharField(_(u"商品影片連結"), max_length=50)
    size = models.CharField(_(u"size"), max_length=10, null=True, blank=True)
    unit = models.CharField(_(u"單位"), max_length=10)

    class Meta:
        verbose_name = _(u"商品資訊")
        verbose_name_plural = _(u"商品列表")

    def __unicode__(self):
        return self.item_name

class CartItem(models.Model):
    user = models.ForeignKey(User, related_name='user_cart_item')
    product = models.ForeignKey(ProductInfo,  related_name='user_cart_product')
    creation_date = models.DateTimeField(verbose_name=_('creation date'), auto_now=True)
    checked_date = models.DateTimeField(verbose_name=_('creation date'), null=True, blank=True)
    is_checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    amount = models.IntegerField(_(u"數量"))

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('creation_date',)

    def __unicode__(self):
        return u'%d units of %s' % (self.amount, self.product.__class__.__name__)

class PayMentRecord(models.Model):
    product = models.ManyToManyField(ProductInfo,  related_name='record_product')
    cart = models.ManyToManyField(CartItem,  related_name='record_cart_item')
    user = models.ForeignKey(User,  related_name='user_payment_record')
    total_amount = models.IntegerField(_(u"總金額"))
    date = models.DateTimeField(_(u"建立時間"), auto_now=True)
    order_id = models.CharField(_(u"訂單編號"), max_length=30)
    is_checked = models.BooleanField(_(u"是否已付款"), default=False)
    checked_time = models.DateTimeField(_(u"付款時間"), null=True, blank=True)
    #invoice = models.OneToOneField(PayMentInvoice,  related_name='payment_record_invoice', null=True, blank=True)

class PayMentInvoice(models.Model):
    relate_number = models.CharField(_(u"自訂編號"), max_length=30, null=True, blank=True)
    invoice_type = models.IntegerField(_(u"發票方式"), choices=INVOICE_TYPE_CHOICES)
    invoice_kind = models.IntegerField(_(u"發票類型"), choices=INVOICE_KIND_CHOICES)
    print_type = models.CharField(_(u"索取紙本"), choices=PRINT_TYPE_CHOICES, max_length=1, null=True, blank=True)
    donation = models.CharField(_(u"捐贈"), choices=DONATION_CHOICES, max_length=1, null=True, blank=True)
    love_code = models.CharField(_(u"愛心碼"), max_length=7, null=True, blank=True)
    carruer_type = models.CharField(_(u"載具類別"), choices=CARRUER_TYPE_CHOICES, max_length=1, null=True, blank=True)
    carruer_num = models.CharField(_(u"載具編號"), max_length=64 , null=True, blank=True)
    tax_type = models.CharField(_(u"課稅類別"), max_length=1 , null=True, blank=True)
    inv_type = models.CharField(_(u"字軌類別"), max_length=2 , null=True, blank=True)
    invoice_rtn_msg = models.CharField(_(u"回應訊息"), max_length=200 , null=True, blank=True)
    invoice_date = models.DateTimeField(_(u"發票開立時間"), null=True, blank=True)
    random_number = models.CharField(_(u"隨機碼"), max_length=4 , null=True, blank=True)
    invalid_reason = models.CharField(_(u"作廢原因"), max_length=20 , null=True, blank=True)
    invalid_rtn_code = models.IntegerField(_(u"作廢回應代碼"), null=True, blank=True)
    invalid_rtn_msg = models.CharField(_(u"作廢回應訊息"), max_length=200 , null=True, blank=True)
    invalid_time = models.DateTimeField(_(u"作廢時間"), null=True, blank=True)
    invoice_number = models.CharField(_(u"發票號碼"), max_length=10, null=True, blank=True)
    record = models.OneToOneField(PayMentRecord,  related_name='payment_record_', null=True, blank=True)
    def __unicode__(self):
        return self.invoice_number



class FavoriteItem(models.Model):
    user = models.ForeignKey(User, related_name='user_favorite_item')
    product = models.ForeignKey(ProductInfo,  related_name='user_favorite_product')

