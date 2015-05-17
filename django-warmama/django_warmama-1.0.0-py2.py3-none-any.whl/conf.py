from django.conf import settings as user_settings
__all__ = [
    'settings',
]


DEFAULTS = {
    # PlayerSession ticket lifetime in seconds
    'WARMAMA_TICKET_EXPIRATION': 60,

    # If `True`, ClientLogin requests have username/password validated
    # by a remote url
    'WARMAMA_REMOTE_CLIENTAUTH': False,
    'WARMAMA_AUTH_URL': 'http://remote.auth.server/getauth',

    # Server port to assume if none given
    'WARMAMA_DEFAULT_SERVER_PORT': 44400,
}


class Settings(object):
    """Settings object to map settings to properties"""
    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid setting %s' % attr)

        try:
            return getattr(user_settings, attr)
        except AttributeError:
            return DEFAULTS[attr]


settings = Settings()
