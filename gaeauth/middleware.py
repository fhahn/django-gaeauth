from google.appengine.api import oauth
from google.appengine.api import users
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.middleware import RemoteUserMiddleware


class BaseGoogleRemoteUserMiddleware(RemoteUserMiddleware):
    def get_current_user(self):
        raise NotImplementedError

    def is_current_user_admin(self):
        raise NotImplementedError

    def process_request(self, request):
        user = self.get_current_user()
        if not user:
            # leave request.user set to AnonymousUser by the
            # AuthenticationMiddleware.
            return
        # If the user is already authenticated and that user is the user we get
        # back from get_current_user(), then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.username == self.clean_username(user, request):
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(user=user,
                                 admin=self.is_current_user_admin())
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)


class GoogleRemoteUserMiddleware(BaseGoogleRemoteUserMiddleware):
    def get_current_user(self):
        return users.get_current_user()

    def is_current_user_admin(self):
        return users.is_current_user_admin()


class GoogleOAuthRemoteUserMiddleware(BaseGoogleRemoteUserMiddleware):
    def get_current_user(self):
        try:
            scope = getattr(settings, 'REMOTE_USER_OAUTH_SCOPE', None)
            return oauth.get_current_user(_scope=scope)
        except oauth.Error:
            return None

    def is_current_user_admin(self):
        try:
            return oauth.is_current_user_admin()
        except oauth.Error:
            return False

