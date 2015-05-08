import json
import logging
import os

_log = logging.getLogger(__name__)


class Settings:
    """
    Settings class for tinbox, handles loading and validation of settings.

    Uses self.__dict__ to store settings, providing instance-variable access
    to the settings. e.g. ``settings.client_id  # returns client id``.
    """
    required = ['base_url', 'client_id', 'client_secret', 'scope']

    def __init__(self, settings_dict):
        missing = []

        for key in self.required:
            if key not in settings_dict:
                missing.append(key)

        if missing:
            raise ValueError('The field(s) %r are missing from your tinbox '
                             'settings file.' % missing)

        self.__dict__ = settings_dict

    def get_url(self, path):
        return self.base_url + path

    @classmethod
    def from_file(cls, filename):
        return cls(json.load(open(filename, 'r')))


def get_settings():
    trak_settings_file = os.environ.get('TRAK_SETTINGS')
    settings_file = os.environ.get('TINBOX_SETTINGS', trak_settings_file)

    if settings_file is None:
        raise ValueError('TINBOX_SETTINGS missing from environment, can\'t '
                         'initialize.')

    return Settings.from_file(settings_file)