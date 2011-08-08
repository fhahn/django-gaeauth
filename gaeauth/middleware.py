from google.appengine.api import users
from django.contrib import auth
from django.contrib.auth.middleware import RemoteUserMiddleware


class GoogleRemoteUserMiddleware(RemoteUserMiddleware):
    def get_current_user(self):
        return users.get_current_user()

    def is_current_user_admin(self):
        return users.is_current_user_admin()

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
