from django.conf.urls.defaults import *
from django.contrib.auth.tests import urls as auth_urls
from gaeauth import urls as gaeauth_urls

urlpatterns = auth_urls.urlpatterns + patterns('',
    url('^gaeauth/', include(gaeauth_urls)),
)
