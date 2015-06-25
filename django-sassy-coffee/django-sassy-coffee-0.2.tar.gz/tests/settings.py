# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',  # Or path to database file if using sqlite3.
    }
}

SECRET_KEY = 'sassycoffee123'

STATIC_ROOT = os.path.join(BASE_DIR, 'data')
STATIC_URL = '/data/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

DJANGO_SASSY_COFFEE_FORMATS = [
    'sass',
    'coffee'
]

DJANGO_SASSY_COFFEE_EXCLUSIONS = [
    'base.sass'
]
