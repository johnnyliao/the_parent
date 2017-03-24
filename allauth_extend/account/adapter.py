from allauth.account.adapter import DefaultAccountAdapter, resolve_url, warnings
from allauth.utils import get_user_model
import settings

class NicokimAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.GET['next']:
            return request.GET['next']
        else:
            url = settings.LOGIN_REDIRECT_URL
        return resolve_url(url)

