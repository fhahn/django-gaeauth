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

        username = self.clean_username(g_user.email())

        if hasattr(settings, 'ALLOWED_USERS'):
            try:
                settings.ALLOWED_USERS.index(username)
            except ValueError:
                return None

        user, created = User.objects.get_or_create(password=g_user.user_id())
        if user.email != g_user.email():
            # User object was just created, or their username/email has changed
            # since the last time they authenticated.
            user.email = g_user.email()
            user.username = username
            user.save()
        if created:
            user = self.configure_user(user)
        return user

    def clean_username(self, username):
        return username.split('@')[0]

    def configure_user(self, user):
        if users.is_current_user_admin():
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user
