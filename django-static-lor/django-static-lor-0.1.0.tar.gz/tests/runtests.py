#!/usr/bin/env python

import os
import sys
import django
from django.conf import settings
from django.test.runner import DiscoverRunner

here = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(here)
sys.path[0:0] = [here, parent]

LOR_FILES_URLS = {
    'testfile': ('testfile.txt', '/textfile.txt'),
    'localisnone': (None, '/textfile.txt'),
    'localnewdir': ('newdir/testfile.txt', '/textfile.txt'),
    'remoteisnone': ('testfile.txt', None),
    'noremote': ('testfile.txt',),
}

settings.configure(
    STATIC_ROOT='/tmp/',
    STATIC_URL='/static/',
    LOR_STATIC_DIR='/tmp/lor_test/',
    LOR_LOCAL_URLS=True,
    LOR_FILES_URLS=LOR_FILES_URLS,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    INSTALLED_APPS=["lor", "testapp"],
    MIDDLEWARE_CLASSES=(),
    ROOT_URLCONF='testapp.urls',
    SECRET_KEY="it's a secret to everyone",
    SITE_ID=1,
)


def main():
    if django.VERSION >= (1, 7):
        django.setup()
    runner = DiscoverRunner(failfast=True, verbosity=1)
    failures = runner.run_tests(['testapp'], interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()
