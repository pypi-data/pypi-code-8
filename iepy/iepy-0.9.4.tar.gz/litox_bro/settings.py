"""
Django settings for webui project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from iepy.webui.webui.settings import *

IEPY_VERSION = '0.9'
SECRET_KEY = '%dhn0+g#0+1u@*91)6!fa9h0hjlb#u$28aiwg+!(yarp=(r#cl'
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/jmansilla/projects/iepy/repo/litox/litox.sqlite',
    }
}
IEPY_VERSION = '0.9.2'  # Remove line declaring the old IEPY_VERSION above.
