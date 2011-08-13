from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.core.urlresolvers import reverse
from django.contrib.auth import   REDIRECT_FIELD_NAME
from django.test import TestCase

from google.appengine.api import users

from gaeauth.tests.gae import GaeUserApiTestMixin
from gaeauth.utils import get_google_login_url

class GaeauthViewsTest(GaeUserApiTestMixin, TestCase):
    urls = 'gaeauth.tests.urls'

    def setUp(self):
        super(GaeauthViewsTest, self).setUp()
        self.login_url = reverse('google_login')
        self.logout_url = reverse('google_logout')
        self.authenticate_url = reverse('google_authenticate')

        settings.AUTHENTICATION_BACKENDS = (
            'gaeauth.backends.GoogleAccountBackend',
        )
        self.user = users.User(
            email='foo@example.com', _auth_domain='example.com', _user_id=12345)

    def get_google_login_url(self, next):
        '''
        calls gaeauth.utils.get_google_login_url with REDIRECT_FIELD_NAME
        parameter
        '''
        return get_google_login_url(REDIRECT_FIELD_NAME, next)

    def test_login_with_invalid_next_param(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.get_google_login_url('/'), response['Location'])
        response = self.client.get(self.login_url, {'next': 'http://host'})
        self.assertEquals(self.get_google_login_url('/'), response['Location'])
        response = self.client.get(self.login_url, {'next': '/space path'})
        self.assertEquals(self.get_google_login_url('/'), response['Location'])
 
    def test_login_with_valid_next_param(self):
        response = self.client.get(self.login_url, {'next': '/foo'})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.get_google_login_url('/foo'),
                          response['Location'])
            
    def test_logout(self):
        self.client.login(user=self.user)
        self.assert_(SESSION_KEY in self.client.session)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assert_(SESSION_KEY not in self.client.session)

    def test_authenticate(self):
        self.assert_(SESSION_KEY not in self.client.session)
        self.login_user('foo@example.com', '123456')
        response = self.client.get(self.authenticate_url, {'next': '/foo'})
        self.assert_(SESSION_KEY in self.client.session)
        self.assertEqual(response.status_code, 302)
        self.assert_('/foo' in response['Location'])

    def test_authenticate_when_django_auth_fails(self):
        response = self.client.get(self.authenticate_url, {'next': '/foo'})
        self.assertEqual(response.status_code, 302)
        self.assert_('/invalid' in response['Location'])
        
