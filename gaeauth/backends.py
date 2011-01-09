from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from google.appengine.api import users


class GoogleAccountBackend(ModelBackend):
    """
    backend for authentication via Google Accounts on Google
    App Engine

    A Django auth.contrib.models.User object is linked to
    a Google Account via the password field, that stores
    the unique Google Account ID
    The Django User object is created the first time a user logs
    in with his Google Account.
    """

    def authenticate(self, **credentials):
        g_user = users.get_current_user()

        if g_user == None:
            return None

        username = g_user.email().split('@')[0]

        if hasattr(settings, 'ALLOWED_USERS'):
            try:
                settings.ALLOWED_USERS.index(username)
            except ValueError:
                return None
            
        try:
            user = User.objects.get(password=g_user.user_id())
            if user.email is not g_user.email():
                user.email = g_user.email()
                user.username = username
                user.save()
 
            return user
        except User.DoesNotExist:
                user = User.objects.create_user(username,\
                                                g_user.email())
                user.password = g_user.user_id()
                if users.is_current_user_admin():
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
                return user
