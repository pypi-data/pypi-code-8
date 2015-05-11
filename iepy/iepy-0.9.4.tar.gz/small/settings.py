"""
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from iepy.webui.webui.settings import *

IEPY_VERSION = '0.9.2'
IEPY_LANG = 'en'
SECRET_KEY = '$x6^4@28neq9(6!sco3k+0i-+%s)hem+wa^*&1cm(lubk(z&cz'
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/jmansilla/projects/iepy/repo/small/small.sqlite',
#        "ENGINE": "django.db.backends.postgresql_psycopg2",
#        'NAME': 'debug_m_11_go',
    }
}
