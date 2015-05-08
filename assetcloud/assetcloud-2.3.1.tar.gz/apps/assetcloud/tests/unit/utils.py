# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Utility methods and base classes for unit tests.
"""

import django.utils.unittest
from assetcloud import app_settings


class UnitTestCase(django.utils.unittest.TestCase):
    """
    Base for all unit level tests.
    """
    tags = ['unit', ]


class OverrideAssetcloudSettings(object):
    original_settings = {}

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, function):
        def wrapped(*args, **kwargs):
            self._update_assetcloud_settings()
            result = function(*args, **kwargs)
            self._revert_to_original_settings()
            return result
        return wrapped

    def _update_assetcloud_settings(self):
        for key, value in self.kwargs.iteritems():
            self.original_settings[key] = getattr(app_settings, key, '')
            setattr(app_settings, key, value)

    def _revert_to_original_settings(self):
        for key, value in self.original_settings.iteritems():
            setattr(app_settings, key, value)
