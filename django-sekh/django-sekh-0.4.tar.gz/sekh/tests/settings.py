"""Settings for testing django-sekh"""

DATABASES = {
    'default': {'NAME': ':memory:',
                'ENGINE': 'django.db.backends.sqlite3'}}

SECRET_KEY = 'secret-key'

INSTALLED_APPS = ['sekh']
