# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""Test Setup of customer.mlscrcom."""

# python imports
import unittest2 as unittest

# zope imports
from plone.browserlayer import utils as layerutils

# local imports
from customer.mlscrcom.browser.interfaces import ICustomerSpecific
from customer.mlscrcom.testing import CUSTOMER_MLSCRCOM_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):
    """Setup Test Case for customer.mlscrcom."""
    layer = CUSTOMER_MLSCRCOM_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']

    def test_plone_app_registry_installed(self):
        """Test that plone.app.registry is installed."""
        qi = self.portal.portal_quickinstaller
        if qi.isProductAvailable('plone.app.registry'):
            self.assertTrue(qi.isProductInstalled('plone.app.registry'))
        else:
            self.assertTrue('plone.app.registry' in
                            qi.listInstallableProfiles())

    def test_plone_app_theming_installed(self):
        """Test that plone.app.theming is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.app.theming'))

    def test_plonepolicy_realestate_installed(self):
        """Test that plonepolicy.realestate is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plonepolicy.realestate'))

    def test_products_doormat_installed(self):
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled(
            'Doormat'))

    def test_products_linguaplone_installed(self):
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled(
            'LinguaPlone'))

    def test_browserlayer_installed(self):
        self.assertTrue(ICustomerSpecific in layerutils.registered_layers())
