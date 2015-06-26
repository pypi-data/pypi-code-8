#coding=utf-8
"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ secret_key }}'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# TEMPLATE_DEBUG = True

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '{{ project_name }}.urls'

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-CN'

# For utf8mb4 support
import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/
STATIC_URL = '/static/'

#
# Log settings
#
logger = logging.getLogger('default_log')
# logger_monitor = logging.getLogger('monitor')
# mail_logger = logging.getLogger('mail_log')
# mongo_logger = logging.getLogger('log2mongo')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'plain': {
            'format': '%(asctime)s %(message)s'
        },
        'standard': {
            "format": '%(levelname)s %(asctime)s [%(module)s.%(funcName)s line:%(lineno)d] %(message)s',
        },
    },
    'filters': {
    },
    'handlers': {
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html': True,
        # },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'logs' 'info.log'),  # 或者直接写路径：'c://logs/all.log',
            'maxBytes': 1024 * 1024 * 10,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'exception': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'logs' 'exception.log'),  # 或者直接写路径：'c://logs/all.log',
            'maxBytes': 1024 * 1024 * 10,  # 5 MB
            'backupCount': 5,
            'formatter': 'plain',
        },
        # 'request_handler': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(LOG_DIR, 'logs' 'debug.log'),  # 或者直接写路径：'filename':'c:/logs/request.log''
        #     'maxBytes': 1024 * 1024 * 5,  # 5 MB
        #     'backupCount': 5,
        #     'formatter': 'standard',
        # },
        # 'scprits_handler': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(LOG_DIR, 'script.log'),  # 或者直接写路径：'filename':'c:/logs/script.log'
        #     'maxBytes': 1024 * 1024 * 5,  # 5 MB
        #     'backupCount': 5,
        #     'formatter': 'standard',
        # },
        # 'timelog': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(LOG_DIR, 'timeout.log'),
        #     'maxBytes': 1024 * 1024 * 5,  # 5 MB
        #     'backupCount': 5,
        #     'formatter': 'plain',
        # },
        # 'monitor_handler': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(LOG_DIR, 'monitor.log'),
        #     'maxBytes': 1024 * 1024 * 5,
        #     'backupCount': 5,
        #     'formatter': 'standard',
        # },
        # 'log2mongo_handler': {
        #     'level': 'INFO',
        #     'class': "log4mongo.handlers.MongoHandler",
        #     'database_name': 'logs',
        #     'collection': '{{ project_name }}_online',
        # },
    },
    'loggers': {
        'default_log': {
            'handlers': [
                'default', 'exception',
            ],
            'level': 'INFO',
            'propagate': False
        },
        # 'mail_log': {
        #     'handlers': [
        #         'mail_admins'
        #     ],
        #     'level': 'INFO',
        #     'propagate': False
        # },
        # 'django.request': {
        #     'handlers': [
        #         'request_handler'
        #     ],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
        # 'scripts': {  # 脚本专用日志
        #               'handlers': [
        #                   'scprits_handler'],
        #               'level': 'INFO',
        #               'propagate': False
        # },
        # 'monitor': {
        #     'handlers': [
        #         'monitor_handler'
        #     ],
        #     'level': 'INFO',
        #     'propagate': False,
        # },
        # 'log2mongo': {
        #     'level': 'INFO',
        #     'handlers': [
        #         'log2mongo_handler'
        #     ],
        # },
        # 'timelog.middleware': {
        #     'handlers': [
        #         'timelog'
        #     ],
        #     'level': 'DEBUG',
        #     'propogate': False,
        # }
    }
}

# 根据环境不同引用不同的扩展settings
server_env = None
if os.path.exists(BASE_DIR, 'server_tag_local'): 
    server_env = 'local'
    from settings_local import *
if os.path.exists(BASE_DIR, 'server_tag_online'): 
    server_env = 'online'
    from settings_online import *
if os.path.exists(BASE_DIR, 'server_tag_dev'): 
    server_env = 'dev'
    from settings_dev import *
if os.path.exists(BASE_DIR, 'server_tag_release'):
    server_env = 'release'
    from settings_release import *
if server_env is None:
    print u'''
        项目根目录缺少环境标志文件(server_tag_{ENV})
        ENV:
            local: 本地
            online: 生产环境
            dev: 开发调试环境
            release: release环境
        注：也可根据个人需求定制不同环境
    '''
