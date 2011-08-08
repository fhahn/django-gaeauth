import urllib

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from google.appengine.api import users
from google.appengine.ext import testbed
from flexmock import flexmock


class GaeauthViewsTest(TestCase):
    urls = 'gaeauth.tests.urls'

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()
        settings.AUTHENTICATION_BACKENDS = (
            'gaeauth.backends.GoogleAccountBackend',
        )
        flexmock(users).should_receive('get_current_user').and_return(
            users.User(email='foo@example.com', _auth_domain='example.com',
                       _user_id=12345))

    def tearDown(self):
        self.testbed.deactivate()

    def test_login_with_invalid_next_param(self):
        response = self.client.get('/gaeauth/login/')
        self.assertEqual(response.status_code, 302)
        self.assert_(urllib.quote('/gaeauth/authenticate/?next=/') in
                     response['Location'])
        response = self.client.get('/gaeauth/login/', {'next': 'http://host'})
        self.assert_(urllib.quote('/gaeauth/authenticate/?next=/') in
                     response['Location'])
        response = self.client.get('/gaeauth/login/', {'next': '/space path'})
        self.assert_(urllib.quote('/gaeauth/authenticate/?next=/') in
                     response['Location'])

    def test_login_with_valid_next_param(self):
        response = self.client.get('/gaeauth/login/', {'next': '/foo'})
        self.assertEqual(response.status_code, 302)
        self.assert_(urllib.quote('/gaeauth/authenticate/?next=/foo') in
                     response['Location'])

    def test_logout(self):
        self.client.login()
        self.assert_(SESSION_KEY in self.client.session)
        response = self.client.get('/gaeauth/logout/')
        self.assertEqual(response.status_code, 302)
        self.assert_(SESSION_KEY not in self.client.session)

    def test_authenticate(self):
        self.assert_(SESSION_KEY not in self.client.session)
        response = self.client.get('/gaeauth/authenticate/', {'next': '/foo'})
        self.assert_(SESSION_KEY in self.client.session)
        self.assertEqual(response.status_code, 302)
        self.assert_('/foo' in response['Location'])

    def test_authenticate_when_django_auth_fails(self):
        users.should_receive('get_current_user').and_return(None)
        response = self.client.get('/gaeauth/authenticate/', {'next': '/foo'})
        self.assertEqual(response.status_code, 302)
        self.assert_('/invalid' in response['Location'])
