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

    def authenticate(self, user=None, admin=False, **credentials):
        """Authenticate the given user.

        Args:
          user: The google.appengine.api.users.User object representing the
              current App Engine user.
          admin: Whether the current user is an developer/admin of the
              application.
        """
        if user is None:
            return None

        username, domain = user.email().split('@')

        # Check for settings whitelists.
        for setting, value in (('ALLOWED_USERS', username),
                               ('ALLOWED_DOMAINS', domain)):
            if (hasattr(settings, setting) and
                value not in getattr(settings, setting)):
                return None

        django_user, created = User.objects.get_or_create(
            password=user.user_id(), defaults={'email': user.email(),
                                               'username': username})
        if django_user.email != user.email():
            # User object was just created, or their username/email has changed
            # since the last time they authenticated.
            django_user.email = user.email()
            django_user.username = username
            django_user.save()
        if created:
            django_user = self.configure_user(django_user, admin)
        return django_user

    def clean_username(self, username):
        return username.split('@')[0]

    def configure_user(self, user, admin):
        if admin:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user
