from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase

from google.appengine.api import users

from gaeauth.backends import GoogleAccountBackend
from gaeauth.tests.gae import GaeUserApiTestMixin


class GoogleAccountBackendTest(GaeUserApiTestMixin, TestCase):
    def setUp(self):
        super(GoogleAccountBackendTest, self).setUp()
        settings.AUTHENTICATION_BACKENDS = (
            'gaeauth.backends.GoogleAccountBackend',
        )
        self.email = 'foo@example.com'
        self.auth_domain = 'example.com'
        self.user_id = '12345'
        self.user = users.User(
            email=self.email, _auth_domain=self.auth_domain,
            _user_id=self.user_id)
        

    def test_clean_username(self):
        self.login_user(self.email, self.user_id)
        backend = GoogleAccountBackend()
        self.assertEqual('foo', backend.clean_username('foo@example.com'))

    def test_authenticate(self):
        user = auth.authenticate(user=self.user)
        self.assertEqual('foo', user.username)

    def test_allowed_users(self):
        """Tests for when user has supplied an ALLOWED_USERS settings entry."""
        settings.ALLOWED_USERS = ('bar',)
        self.assertIsNone(auth.authenticate(user=self.user))
        user2 = users.User(
            email='bar@example.com', _auth_domain='example.com', _user_id=67890)
        self.assertEqual('bar', auth.authenticate(user=user2).username)
        del settings.ALLOWED_USERS

    def test_allowed_domains(self):
        """Tests when user has supplied an ALLOWED_DOMAINS settings entry."""
        settings.ALLOWED_DOMAINS = ('fail.example.com',)
        self.assertIsNone(auth.authenticate(user=self.user))
        settings.ALLOWED_DOMAINS = ('example.com',)
        self.assertEqual('foo', auth.authenticate(user=self.user).username)
        del settings.ALLOWED_DOMAINS

    def test_configure_user(self):
        """Tests that App Engine admin User object gets staff/superuser."""
        user = User.objects.create(username='test')
        backend = GoogleAccountBackend()
        backend.configure_user(user, True)
        user = User.objects.get(username='test')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_change(self):
        """Tests that user's email and username are properly updated."""
        User.objects.create(
            username='old', email='old@example.com', password=12345)
        auth.authenticate(user=self.user)
        user = User.objects.get(password=12345)
        self.assertEqual('foo', user.username)
        self.assertEqual('foo@example.com', user.email)

    def test_empty_username_exists(self):
        """Tests that an existing empty username User does not break backend."""
        # Regression test for https://bitbucket.org/fhahn/django-gaeauth/issue/1
        User.objects.create()
        self.assertEqual('foo', auth.authenticate(user=self.user).username)

