"""
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from iepy.webui.webui.settings import *

IEPY_VERSION = '0.9.2'
SECRET_KEY = '&1&@i#wfsn(+21ti#6)gjgmmx_^trmzrgl-ujf$mnwp$_@41@3'
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'grammar_orgloc',
        'USER': 'jmansilla',
        'PASSWORD': 'montoto'
    }
}
