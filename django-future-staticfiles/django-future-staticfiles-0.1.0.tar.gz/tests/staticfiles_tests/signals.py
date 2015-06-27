import os
import threading
import time

from django.conf import settings
from django.db import connections
from django.dispatch import receiver
from django.test.signals import setting_changed
from django.utils import timezone
from django.utils.functional import empty

# Most setting_changed receivers are supposed to be added below,
# except for cases where the receiver is related to a contrib app.


@receiver(setting_changed)
def clear_cache_handlers(**kwargs):
    if kwargs['setting'] == 'CACHES':
        from django.core.cache import caches
        caches._caches = threading.local()


@receiver(setting_changed)
def update_connections_time_zone(**kwargs):
    if kwargs['setting'] == 'TIME_ZONE':
        # Reset process time zone
        if hasattr(time, 'tzset'):
            if kwargs['value']:
                os.environ['TZ'] = kwargs['value']
            else:
                os.environ.pop('TZ', None)
            time.tzset()

        # Reset local time zone cache
        timezone.get_default_timezone.cache_clear()

    # Reset the database connections' time zone
    if kwargs['setting'] == 'USE_TZ' and settings.TIME_ZONE != 'UTC':
        USE_TZ, TIME_ZONE = kwargs['value'], settings.TIME_ZONE
    elif kwargs['setting'] == 'TIME_ZONE' and not settings.USE_TZ:
        USE_TZ, TIME_ZONE = settings.USE_TZ, kwargs['value']
    else:
        # no need to change the database connnections' time zones
        return
    tz = 'UTC' if USE_TZ else TIME_ZONE
    for conn in connections.all():
        conn.settings_dict['TIME_ZONE'] = tz
        tz_sql = conn.ops.set_time_zone_sql()
        if tz_sql:
            conn.cursor().execute(tz_sql, [tz])


@receiver(setting_changed)
def clear_serializers_cache(**kwargs):
    if kwargs['setting'] == 'SERIALIZATION_MODULES':
        from django.core import serializers
        serializers._serializers = {}


@receiver(setting_changed)
def language_changed(**kwargs):
    if kwargs['setting'] in ['LANGUAGES', 'LANGUAGE_CODE', 'LOCALE_PATHS']:
        from django.utils.translation import trans_real
        trans_real._default = None
        trans_real._active = threading.local()
    if kwargs['setting'] in ['LANGUAGES', 'LOCALE_PATHS']:
        from django.utils.translation import trans_real
        trans_real._translations = {}
        trans_real.check_for_language.cache_clear()


@receiver(setting_changed)
def file_storage_changed(**kwargs):
    file_storage_settings = [
        'DEFAULT_FILE_STORAGE',
        'FILE_UPLOAD_DIRECTORY_PERMISSIONS',
        'FILE_UPLOAD_PERMISSIONS',
        'MEDIA_ROOT',
        'MEDIA_URL',
    ]

    if kwargs['setting'] in file_storage_settings:
        from django.core.files.storage import default_storage
        default_storage._wrapped = empty


@receiver(setting_changed)
def root_urlconf_changed(**kwargs):
    if kwargs['setting'] == 'ROOT_URLCONF':
        from django.core.urlresolvers import clear_url_caches, set_urlconf
        clear_url_caches()
        set_urlconf(None)


@receiver(setting_changed)
def static_storage_changed(**kwargs):
    if kwargs['setting'] in [
        'STATICFILES_STORAGE',
        'STATIC_ROOT',
        'STATIC_URL',
    ]:
        from django.contrib.staticfiles.storage import staticfiles_storage
        staticfiles_storage._wrapped = empty
