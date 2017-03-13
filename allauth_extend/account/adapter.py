from allauth.account.adapter import DefaultAccountAdapter, resolve_url, warnings
from allauth.utils import get_user_model
import settings

class NicokimAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        url = getattr(settings, "LOGIN_REDIRECT_URLNAME", None)
        if url:
            print "url exsits"
            print url
            warnings.warn("LOGIN_REDIRECT_URLNAME is deprecated, simply"
                          " use LOGIN_REDIRECT_URL with a URL name",
                          DeprecationWarning)
        else:
            url = settings.LOGIN_REDIRECT_URL
            print "settings url"
            print url
        return resolve_url(url)

    def new_user(self, request):
        if not request.user.is_anonymous():
            user = request.user
        else:
            user = get_user_model()()
        print "new user"
        print user
        return user

    def save_user(self, request, user, form, commit=True):
        print "save user"
        print form.cleaned_data

        return super(NicokimAccountAdapter, self).save_user(request, user, form, commit)
