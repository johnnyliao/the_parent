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

    def authentication_error(self,
                             request,
                             provider_id,
                             error=None,
                             exception=None,
                             extra_context=None):
        """
        Invoked when there is an error in the authentication cycle. In this
        case, pre_social_login will not be reached.

        You can use this hook to intervene, e.g. redirect to an
        educational flow by raising an ImmediateHttpResponse.
        """
        print "request"
        print request
        print "\n\n"
        print
        "provider_id"
        print provider_id
        print "\n\n"
        print "error"
        print error
        print "\n\n"
        print "exception"
        print exception
        print "\n\n"
        print "extra_context"
        print extra_context
        pass