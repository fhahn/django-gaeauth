# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('',
   url(r'^login/$', 'gaeauth.views.login', name='google_login'),
   url(r'^logout/$', 'gaeauth.views.logout', name='google_logout'),
   url(r'^authenticate/$', 'gaeauth.views.authenticate', name='google_authenticate'),
)
