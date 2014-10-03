#!/bin/bash

# fetch dependencies
if [ ! -f django-nonrel.zip ]; then
    wget -O django-nonrel.zip https://github.com/django-nonrel/django/zipball/nonrel-1.5
    unzip -q django-nonrel.zip
fi

if [ ! -f djangoappengine.zip ]; then
    wget -O djangoappengine.zip https://github.com/django-nonrel/djangoappengine/zipball/master
    unzip -q djangoappengine.zip
fi

if [ ! -f djangotoolbox.zip ]; then
    wget -O djangotoolbox.zip https://github.com/django-nonrel/djangotoolbox/zipball/master
    unzip -q djangotoolbox.zip
fi

if [ ! -f google_appengine.zip ]; then
    wget -O google_appengine.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.12.zip
    unzip -q google_appengine.zip
fi

# add stuff to PYTHONPATH
export PYTHONPATH="$PYTONPATH:\
`python -c 'import glob; import os; print(os.path.abspath(glob.glob(\"django-nonrel-djangoappengine*\")[0]))'`:\
`python -c 'import glob; import os; print(os.path.abspath(glob.glob(\"django-nonrel-django-*\")[0]))'`:\
`python -c 'import glob; import os; print(os.path.abspath(glob.glob(\"django-nonrel-djangotoolbox*\")[0]))'`:\
`pwd`/google_appengine:\
`pwd`/google_appengine/lib/yaml/lib/"

# run the tests
python2 runtests.py
