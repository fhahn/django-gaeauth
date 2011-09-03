Django Gaeauth
=======================
An authentication backend, for login via Google Accounts on Google Appengine. 
Django-gaeauth uses the Google App Engine Users_ and Oauth_ API, so it only works on Google App Engine.
You will also need the Djangoappengine backend for Django-Nonrel_.

.. _Users https://code.google.com/appengine/docs/python/users/functions.html
.. _Oauth https://code.google.com/appengine/docs/python/oauth/functions.html
.. _Djangoappengine http://www.allbuttonspressed.com/projects/djangoappengine
.. _Django-Nonrel http://www.allbuttonspressed.com/projects/django-nonrel


Installation
============

 - get the code:
   .. sourcecode:: bash

      git clone https://fhahn@github.com/fhahn/django-gaeauth.git
   
 - add the authentication backend **gaeauth.backends.GoogleAccountBackend** to your settings.py

  .. sourcecode:: python

      settings.py:

      AUTHENTICATION_BACKENDS = (
          'gaeauth.backends.GoogleAccountBackend',
      )

 - include **gaeauth.urls** in your urlconf to **login**, **logout** and **authenticate**
  
  .. sourcecode:: python

      urls.py:
   
      (r'^accounts/', include('gaeauth.urls')),

   
   Now you can use **/accounts/login/** to use Google Accounts for login and **/accounts/logout/** to log out. 
