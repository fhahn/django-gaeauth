from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from flexmock import flexmock
from gaeauth.backends import GoogleAccountBackend
from google.appengine.api import users


class GoogleAccountBackendTest(TestCase):
    def setUp(self):
        settings.AUTHENTICATION_BACKENDS = (
            'gaeauth.backends.GoogleAccountBackend',
        )
        self.g_user = users.User(
            email='foo@example.com', _auth_domain='example.com', _user_id=12345)
        flexmock(users)

    def test_clean_username(self):
        backend = GoogleAccountBackend()
        self.assertEqual('foo', backend.clean_username('foo@example.com'))

    def test_authenticate(self):
        users.should_receive('get_current_user').and_return(self.g_user)
        user = auth.authenticate()
        self.assertEqual('foo', user.username)

    def test_allowed_users(self):
        """Tests for when user has supplied an ALLOWED_USERS settings entry."""
        settings.ALLOWED_USERS = ('bar',)
        g_user2 = users.User(
            email='bar@example.com', _auth_domain='example.com', _user_id=67890)
        users.should_receive('get_current_user').and_return(
            self.g_user).and_return(g_user2)
        self.assertIsNone(auth.authenticate())
        self.assertEqual('bar', auth.authenticate().username)
        del settings.ALLOWED_USERS

    def test_configure_user(self):
        """Tests that App Engine admin User object gets staff/superuser."""
        users.should_receive('is_current_user_admin').and_return(True)
        user = User.objects.create(username='test')
        backend = GoogleAccountBackend()
        backend.configure_user(user)
        user = User.objects.get(username='test')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_change(self):
        """Tests that user's email and username are properly updated."""
        users.should_receive('get_current_user').and_return(self.g_user)
        User.objects.create(
            username='old', email='old@example.com', password=12345)
        auth.authenticate()
        user = User.objects.get(password=12345)
        self.assertEqual('foo', user.username)
        self.assertEqual('foo@example.com', user.email)

    def test_empty_username_exists(self):
        """Tests that an existing empty username User does not break backend."""
        # Regression test for https://bitbucket.org/fhahn/django-gaeauth/issue/1
        User.objects.create()
        users.should_receive('get_current_user').and_return(self.g_user)
        self.assertEqual('foo', auth.authenticate().username)
