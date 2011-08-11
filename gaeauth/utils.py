from django.core.urlresolvers import reverse

from google.appengine.api import users


def get_google_login_url(redirect_field_name, redirect_to):
    return users.create_login_url('%s?%s=%s' % (reverse('google_authenticate'),
                                         redirect_field_name,
                                         redirect_to))
