"""
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from iepy.webui.webui.settings import *

IEPY_VERSION = '0.9.3'
IEPY_LANG = 'en'
SECRET_KEY = '@vo@ye&edas_fg$=-ci2#ws__o))4fpj(l0e$z@&b0qigkcy^#'
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/jmansilla/projects/iepy/repo/scipyla/scipyla.sqlite',
    }
}
