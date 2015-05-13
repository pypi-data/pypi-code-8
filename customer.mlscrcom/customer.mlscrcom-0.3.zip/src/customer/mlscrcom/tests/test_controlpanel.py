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
"""Test Control Panel for customer.mlscrcom."""

# python imports
import unittest2 as unittest

# zope imports
from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID, logout, setRoles
from zope.component import getMultiAdapter
from zope.interface import directlyProvides

# local imports
from customer.mlscrcom.browser.interfaces import ICustomerSpecific
from customer.mlscrcom.testing import CUSTOMER_MLSCRCOM_INTEGRATION_TESTING


class TestMLSCRComControlPanel(unittest.TestCase):
    """Control Panel Test Case for customer.mlscrcom."""
    layer = CUSTOMER_MLSCRCOM_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']
        directlyProvides(self.portal.REQUEST, ICustomerSpecific)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_mlscrcom_controlpanel_view(self):
        """Test that the mls-cr.com configuration view is available."""
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='mlscrcom-controlpanel')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_mlscrcom_controlpanel_view_protected(self):
        """Test that the mls-cr.com configuration view needs authentication."""
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                          '@@mlscrcom-controlpanel')

    def test_mlscrcom_in_controlpanel(self):
        """Check that there is an mls-cr.com entry in the control panel."""
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.assertTrue('customer_mlscrcom' in [a.getAction(self)['id']
                        for a in self.controlpanel.listActions()])
