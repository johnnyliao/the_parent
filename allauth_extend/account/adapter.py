from allauth.account.adapter import DefaultAccountAdapter, resolve_url, warnings
from allauth.utils import get_user_model
import settings

class NicokimAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        else:
            url = settings.LOGIN_REDIRECT_URL
            print "settings url"
            print url
        return resolve_url(url)

