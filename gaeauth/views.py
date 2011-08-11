from django.http import HttpResponseRedirect
from django.contrib.auth import login as django_login, \
    authenticate as django_authenticate, logout as django_logout, \
    REDIRECT_FIELD_NAME

from google.appengine.api import users

from .utils import get_google_login_url

# redirects to the google user api generated login url
def login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
        redirect_to = '/'
    return HttpResponseRedirect(get_google_login_url(redirect_field_name,
                                                     redirect_to))

# redirects to the google user api generated login url
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(users.create_logout_url("/"))


def authenticate(request):
    user = django_authenticate(
        user=users.get_current_user(), admin=users.is_current_user_admin())
    if user is not None:
        django_login(request, user)
        #redirect to valid logged page (preferably the user's request)
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            redirect_to = '/'
        return HttpResponseRedirect(redirect_to)
    else:
        # return invalid login page
        return HttpResponseRedirect('/invalid')
