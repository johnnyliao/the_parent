import urllib, urllib2
import random, hashlib
import settings

def generate_verify_code():
	verify_code = str(int(random.random() * 9000 + 1000))

	return verify_code

def hash_verify_code(verify_code):
	return hashlib.sha1(verify_code).hexdigest()

def sms_verify_send(to_phone, message):
	if settings.SEND_SMS:
		params = "username=ieach168&password=ieachdodohousebebehouse&"
		params += "dstaddr=" + to_phone + "&"
		params += "smbody=" + urllib.quote(message.encode("big5"))
		
		urllib2.urlopen('http://202.39.48.216/kotsmsapi-1.php?' + params)
	else:
		print message
