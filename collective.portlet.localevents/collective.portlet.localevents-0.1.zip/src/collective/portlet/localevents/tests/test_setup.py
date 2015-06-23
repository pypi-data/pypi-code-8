# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.portlet.localevents.testing import COLLECTIVE_PORTLET_LOCALEVENTS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.portlet.localevents is properly installed."""

    layer = COLLECTIVE_PORTLET_LOCALEVENTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.portlet.localevents is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.portlet.localevents'))

    def test_uninstall(self):
        """Test if collective.portlet.localevents is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.portlet.localevents'])
        self.assertFalse(self.installer.isProductInstalled('collective.portlet.localevents'))

    def test_browserlayer(self):
        """Test that ICollectivePortletLocaleventsLayer is registered."""
        from collective.portlet.localevents.interfaces import ICollectivePortletLocaleventsLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectivePortletLocaleventsLayer, utils.registered_layers())
