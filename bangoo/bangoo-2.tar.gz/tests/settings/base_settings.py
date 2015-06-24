SECRET_KEY = 'aaa'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles',
    'hvad', 'taggit',
    ### Bangoo core modules
    'bangoo.core', 'bangoo.admin', 'bangoo.content', 'bangoo.navigation', 'bangoo.theming', 'bangoo.media',
    ### Bangoo plugins
    'bangoo.blog',
    'tests',
)

MIDDLEWARE_CLASSES = ()

AUTH_USER_MODEL = 'core.User'