INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.auth',
    'django.contrib.admin',
    'django_freezer',
    'django_nose'
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SECRET_KEY = 'djangofreezer'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    },
}

MIDDLEWARE_CLASSES = ()
