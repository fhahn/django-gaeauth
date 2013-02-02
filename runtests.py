#!/usr/bin/env python

import sys

from django.conf import settings
from django.core import management


def runtests(args):
  settings.configure(
      DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
      INSTALLED_APPS=(
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'gaeauth',
      ),
      ROOT_URLCONF='urls')
  management.call_command('test', 'gaeauth', *args)


if __name__ == '__main__':
  runtests(sys.argv[1:])
