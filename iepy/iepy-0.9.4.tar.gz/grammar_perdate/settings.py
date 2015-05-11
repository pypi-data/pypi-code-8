"""
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from iepy.webui.webui.settings import *

IEPY_VERSION = '0.9.2'
SECRET_KEY = 'hpsdmxlx)=8brj)n&5$$kvnhdwfearyi4+hrup580dbv_*mwd+'
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'grammar_perdate',
        'USER': 'jmansilla',
        'PASSWORD': 'montoto'
    }
}
