# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.updatemimetype.testing import COLLECTIVE_UPDATEMIMETYPE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.updatemimetype is properly installed."""

    layer = COLLECTIVE_UPDATEMIMETYPE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.updatemimetype is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.updatemimetype'))

    def test_uninstall(self):
        """Test if collective.updatemimetype is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.updatemimetype'])
        self.assertFalse(self.installer.isProductInstalled(
            'collective.updatemimetype'))

    def test_browserlayer(self):
        """Test that ICollectiveUpdatemimetypeLayer is registered."""
        from collective.updatemimetype.interfaces import (
            ICollectiveUpdatemimetypeLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveUpdatemimetypeLayer,
            utils.registered_layers()
            )
