import os
DEBUG = True
DATABASES = {
    'default':
        {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/piston.db'
    }
}
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/piston.db'
INSTALLED_APPS = (
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.sites',
    'django.contrib.admin',
    'piston3',
    'test_project.apps.testapp',
)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

SITE_ID = 1
ROOT_URLCONF = 'test_project.urls'

MIDDLEWARE_CLASSES = (
    'piston3.middleware.ConditionalMiddlewareCompatProxy',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'piston3.middleware.CommonMiddlewareCompatProxy',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SECRET_KEY = 'bla'
