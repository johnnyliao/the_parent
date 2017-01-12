#-*- encoding: utf-8 -*-

from django.contrib.auth.models import AbstractUser

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.contenttypes import generic

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.sites.models import Site

import urlparse, settings
import datetime
from django.utils import simplejson
from account import sms
import smtplib
from email.mime.text import MIMEText
import pytz

SEX_CHOICES = (
    ("man", _(u"男")),
    ("women", _(u"女"))
)

class User(AbstractUser):
	nickname = models.CharField(_(u"名稱"), max_length=30, null=True, blank=True)
	phone_number = models.CharField(_(u"電話號碼"), max_length=30, null=True, blank=True)
	photo = models.ImageField(upload_to='photos', max_length=255, null=True, blank=True)
	year = models.IntegerField(_(u"年齡"), null=True, blank=True)
	sex = models.CharField(_(u"姓別"), choices=SEX_CHOICES, max_length=10, null=True, blank=True)
	birthday = models.DateTimeField(_(u"生日"), null=True, blank=True)
	address = models.CharField(_(u"地址"), max_length=60, null=True, blank=True)

	def save(self, *args, **kwargs):
		try:
			old_email = User.objects.get(id=self.id).email
			if old_email != self.email:
				self.verify.resend_verify_code()
			super(User, self).save(*args, **kwargs)
		except:
			super(User, self).save(*args, **kwargs)

	def is_verified(self):
		try:
			if self.verify.date_verified:
				return True
			else:
				return False
		except:
			return False

class UserVerify(models.Model):
	user = models.OneToOneField(User, related_name='verify')
	verification_hash = models.CharField(_(u"驗證碼"), max_length= 50, null=False, blank=False)
	send_date = models.DateTimeField(auto_now=True)
	active_minutes = models.IntegerField(_(u"有效時間(單位:分鐘)"), default=10)
	is_send = models.BooleanField(_(u"已發送"), default=False)
	date_verified = models.DateTimeField(null=True, editable=False)

	errors = ''

	def save(self, *args, **kwargs):
		super(UserVerify, self).save(*args, **kwargs)
		if not self.verification_hash:
			self.send_verification_code()

	def is_verify_code_valid(self, verify_code):
		#import pdb;pdb.set_trace()
		#for user in User.objects.exclude(id=self.user.id).filter(email=self.user.email):
		if self.user.is_verified():
			return False
		tz = pytz.timezone('Asia/Taipei')
		now = datetime.datetime.now(tz)
		deleta_time = self.send_date + timezone.timedelta(minutes=self.active_minutes)
		deleta_time = deleta_time.astimezone(tz)
		print now
		print deleta_time
		if now > deleta_time:
			print "out of date"
			raise Exception(_(u"The verify_code is out of date"))
		else:
			print "ok"

		if self.verification_hash == sms.hash_verify_code(verify_code):
			print "true code"
			self.date_verified = now
			self.save(update_fields=['date_verified'])
			print "save ok"
			return True
		else:
			return False

	def resend_verify_code(self):
		self.verification_hash = None
		self.is_send = False
		self.date_verified = None
		self.send_verification_code()

	def generate_verification_code(self):
		verify_code = sms.generate_verify_code()
		self.verification_hash = sms.hash_verify_code(verify_code)

		return verify_code

	def send_verification_code(self):
		print 11111111111
		verify_code = self.generate_verification_code()
		print "email verify_code is "+ verify_code
		try:
			smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
			smtp_obj.starttls()
			smtp_obj.login("epyonss@gmail.com","Liaom4m4760525")

			domain_name = Site.objects.get_current().domain

			html_text = "請點以下連結進行iEach官方帳號email認證<br/><br/><a href="+domain_name.encode('utf-8')+"account/user_verify/?code="+str(verify_code)+">認證email信箱</a><br/><br/>請於10分鐘內進行認證，時間過後此次認證將失效，謝謝"

			msg = MIMEText(html_text,_subtype='html',_charset='utf8')
			msg['Subject'] = 'iEach官方帳號認證'
			me = '樂享數位股份有限公司<epyonss@gmail.com>'
			msg['From'] = me
			msg['To'] = self.user.email

			smtp_obj.sendmail(me,self.user.email,msg.as_string())

			print "send verify email "

			smtp_obj.close()

			self.is_send = True
		except Exception, e:
			self.is_send = False
			self.errors = e.args

		self.save()

		return self.is_send
