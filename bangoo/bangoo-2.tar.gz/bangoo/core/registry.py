import importlib
from collections import OrderedDict

from django.conf import settings


class AppRegistry(object):
    PLUGIN_ATTRIBUTES = ['FRONTEND_URLCONF', 'BACKEND_URLCONF']

    def __init__(self):
        self.apps = OrderedDict()

    def load(self):
        for app_name in settings.INSTALLED_APPS:
            try:
                plugin = importlib.import_module('%s.plugin' % app_name)
                for attr in self.PLUGIN_ATTRIBUTES:
                    if not hasattr(plugin, attr):
                        continue
                self.apps[app_name] = plugin
            except ImportError:
                pass

    def __iter__(self):
        for key, plugin in self.apps.items():
            yield key, plugin
