from django.contrib.auth.middleware import RemoteUserMiddleware


class GoogleRemoteUserMiddleware(RemoteUserMiddleware):
  header = 'USER_EMAIL'
