from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from gaeauth.tests.gae import GaeUserApiTestMixin
from gaeauth.tests.gae import GaeOauthUserApiTestMixin


class GoogleRemoteUserMiddlewareTest(GaeUserApiTestMixin, TestCase):
    urls = 'gaeauth.tests.urls'
    middleware = 'gaeauth.middleware.GoogleRemoteUserMiddleware'
    backend = 'gaeauth.backends.GoogleAccountBackend'

    def setUp(self):
        super(GoogleRemoteUserMiddlewareTest, self).setUp()
        self.curr_middleware = settings.MIDDLEWARE_CLASSES
        self.curr_auth = settings.AUTHENTICATION_BACKENDS
        settings.MIDDLEWARE_CLASSES += (self.middleware,)
        settings.AUTHENTICATION_BACKENDS = (self.backend,)
        self.email = 'user@example.com'


    def tearDown(self):
        super(GoogleRemoteUserMiddlewareTest, self).tearDown()
        settings.MIDDLEWARE_CLASSES = self.curr_middleware
        settings.AUTHENTICATION_BACKENDS = self.curr_auth

    def test_no_google_user(self):
        """
        Tests that no user is created when there is no Google user returned by
        the App Engine users API.
        """
        num_users = User.objects.count()
        response = self.client.get('/remote_user/')
        self.assertTrue(response.context['user'].is_anonymous())
        self.assertEqual(User.objects.count(), num_users)

    def test_unknown_user(self):
        """
        Tests the case where the Google user returned by the App Engine users
        API does not yet exist as a Django User.
        """
        num_users = User.objects.count()
        self.login_user(self.email, '12345')
        response = self.client.get('/remote_user/')
        self.assertEqual(response.context['user'].username, 'user')
        self.assertEqual(User.objects.count(), num_users + 1)
        User.objects.get(username='user')


    def test_known_user(self):
        """
        Tests the case where the Google user already exists as a Django user.
        """
        User.objects.create(username='user', password='12345',
                            email=self.email)
        num_users = User.objects.count()
        self.login_user(self.email, '12345')
        response = self.client.get('/remote_user/')

        self.assertEqual(response.context['user'].username, 'user')
        self.assertEqual(User.objects.count(), num_users)

        # Test that a different user passed in the headers causes the new user
        # to be created.
        email2 = 'user2@example.com'
        self.login_user(email2, '123456')
        response = self.client.get('/remote_user/')
        self.assertEqual(response.context['user'].username, 'user2')
        self.assertEqual(User.objects.count(), num_users + 1)


class GoogleOAuthRemoteUserMiddlewareTest(GaeOauthUserApiTestMixin,
                                          GoogleRemoteUserMiddlewareTest):
    middleware = 'gaeauth.middleware.GoogleOAuthRemoteUserMiddleware'

    def test_no_google_user(self):
        """
        Tests that no user is created when there is an exception raised by the
        App Engine OAuth users API.
        """
        num_users = User.objects.count()
        self.logout_user()
        response = self.client.get('/remote_user/')
        self.assertTrue(response.context['user'].is_anonymous())
        self.assertEqual(User.objects.count(), num_users)
