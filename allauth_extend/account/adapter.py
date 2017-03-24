from allauth.account.adapter import DefaultAccountAdapter, resolve_url, warnings
from allauth.utils import get_user_model
import settings

class NicokimAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        #import pdb;pdb.set_trace()
        if request.META.get('HTTP_REFERER'):
            return request.META.get('HTTP_REFERER')
        else:
            url = settings.LOGIN_REDIRECT_URL
        return resolve_url(url)

