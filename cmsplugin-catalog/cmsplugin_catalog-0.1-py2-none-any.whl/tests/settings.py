LANGUAGE_CODE = 'en'
SECRET_KEY = 'ooinwerOIUBCOWNEoihs0qrnlDFjosdfn(&#(UN(hfosndf'
SITE_ID = 1

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--nologcapture', '--with-id']

MEDIA_ROOT = '/tmp/cmsplugin-catalog/media/'
STATIC_ROOT = '/tmp/cmsplugin-catalog/static/'
ROOT_URLCONF = 'urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django_nose',
    'cms',
    'menus',
    'mptt',
    'cmsplugin_catalog',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
]
