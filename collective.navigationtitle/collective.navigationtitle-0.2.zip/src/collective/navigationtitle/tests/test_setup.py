# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.navigationtitle.testing import COLLECTIVE_NAVIGATIONTITLE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.navigationtitle is properly installed."""

    layer = COLLECTIVE_NAVIGATIONTITLE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.navigationtitle is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.navigationtitle'))

    def test_uninstall(self):
        """Test if collective.navigationtitle is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.navigationtitle'])
        self.assertFalse(self.installer.isProductInstalled('collective.navigationtitle'))

    def test_browserlayer(self):
        """Test that INavigationTitleLayer is registered."""
        from collective.navigationtitle.interfaces import INavigationTitleLayer
        from plone.browserlayer import utils
        self.assertIn(INavigationTitleLayer, utils.registered_layers())
