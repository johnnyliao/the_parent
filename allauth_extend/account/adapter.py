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

    def is_open_for_signup(self, request, sociallogin):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        """
        print "\n\n"
        print "is_open_for_signup"
        return get_account_adapter().is_open_for_signup(request)

    def is_auto_signup_allowed(self, request, sociallogin):
        print "\n\n\n"
        print "is_auto_signup_allowed"
        # If email is specified, check for duplicate and if so, no auto signup.
        auto_signup = app_settings.AUTO_SIGNUP
        if auto_signup:
            email = user_email(sociallogin.user)
            # Let's check if auto_signup is really possible...
            if email:
                if account_settings.UNIQUE_EMAIL:
                    if email_address_exists(email):
                        # Oops, another user already has this address.
                        # We cannot simply connect this social account
                        # to the existing user. Reason is that the
                        # email adress may not be verified, meaning,
                        # the user may be a hacker that has added your
                        # email address to their account in the hope
                        # that you fall in their trap.  We cannot
                        # check on 'email_address.verified' either,
                        # because 'email_address' is not guaranteed to
                        # be verified.
                        auto_signup = False
                        # FIXME: We redirect to signup form -- user will
                        # see email address conflict only after posting
                        # whereas we detected it here already.
            elif app_settings.EMAIL_REQUIRED:
                # Nope, email is required and we don't have it yet...
                auto_signup = False
        return auto_signup

    def validate_disconnect(self, account, accounts):
        """
        Validate whether or not the socialaccount account can be
        safely disconnected.
        """
        print "\n\n"
        print "validate_disconnect"
        if len(accounts) == 1:
            # No usable password would render the local account unusable
            if not account.user.has_usable_password():
                raise ValidationError(_("Your account has no password set"
                                        " up."))
            # No email address, no password reset
            if app_settings.EMAIL_VERIFICATION \
                    == EmailVerificationMethod.MANDATORY:
                if EmailAddress.objects.filter(user=account.user,
                                               verified=True).count() == 0:
                    raise ValidationError(_("Your account has no verified"
                                            " e-mail address."))

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        print "\n\n"
        print "get_connect_redirect_url"
        assert request.user.is_authenticated()
        url = reverse('socialaccount_connections')
        return url

     def populate_user(self,
                      request,
                      sociallogin,
                      data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        print "\n\n"
        print "populate_user"
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        name = data.get('name')
        user = sociallogin.user
        user_username(user, username or '')
        user_email(user, valid_email_or_none(email) or '')
        name_parts = (name or '').partition(' ')
        user_field(user, 'first_name', first_name or name_parts[0])
        user_field(user, 'last_name', last_name or name_parts[2])
        return user

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        You can use this hook to intervene, e.g. abort the login by
        raising an ImmediateHttpResponse

        Why both an adapter hook and the signal? Intervening in
        e.g. the flow from within a signal handler is bad -- multiple
        handlers may be active and are executed in undetermined order.
        """
        print "\n\n"
        print "pre_social_login"
        pass