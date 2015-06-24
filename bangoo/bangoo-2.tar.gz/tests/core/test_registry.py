from django.conf import settings
from django.test import TestCase

from bangoo.core import bangoo_plugins
from bangoo.core.registry import AppRegistry


class BangooRegistryTest(TestCase):
    def test_registry_import(self):
        self.assertIsInstance(bangoo_plugins, AppRegistry)

    def test_iter(self):
        self.assertGreater(len(list(bangoo_plugins)), 0)

        for plugin_name, plugin in bangoo_plugins:
            self.assertIn(plugin_name, settings.INSTALLED_APPS)
            self.assertIsInstance(plugin.FRONTEND_URLCONF, str)