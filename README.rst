=======================
Setup
=======================

 - get the code:

   **hg clone https://fhahn@bitbucket.org/fhahn/django-gaeauth**
   
 - add the authentication backend (*gaeauth.backends.GoogleAccountBackend*) to settings.py
   
   **AUTHENTICATION_BACKENDS = ('gaeauth.backends.GoogleAccountBackend',)**

 - include *gaeauth.urls* in your urlconf to *login*, *logout* and *authenticate*
  
   for example:
   
   **(r'^accounts/', include('gaeauth.urls')),**

   
   Now you can use */accounts/login/* to use Google Accounts for login and */accounts/logout/* to log out. 
