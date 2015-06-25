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
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# local imports
from customer.mlscrcom.testing import CUSTOMER_MLSCRCOM_INTEGRATION_TESTING


class TestSettings(unittest.TestCase):
    """Settings Test Case for customer.mlscrcom."""
    layer = CUSTOMER_MLSCRCOM_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']
        self.p_properties = getToolByName(self.portal, "portal_properties")

    def test_portal_title(self):
        """Test the portal title."""
        self.assertEquals("MLS Costa Rica", self.portal.getProperty('title'))

    def test_portal_description(self):
        """Test the portal description."""
        self.assertEquals("Costa Rica's official Property and Broker Database",
                          self.portal.getProperty('description'))

    def test_email_from_address(self):
        """Test that the correct Site 'From' address is set."""
        self.assertEquals("info@mls-cr.com",
                          self.portal.getProperty("email_from_address"))

    def test_email_from_name(self):
        """Test that the correct Site 'From' name is set."""
        self.assertEquals("mls-cr.com | Site Administrator",
                          self.portal.getProperty("email_from_name"))

    def test_allowed_languages(self):
        """Test the allowed languages for this website."""
        portal_languages = getToolByName(self.portal, 'portal_languages')
        languages = getattr(portal_languages, 'supported_langs')
        self.failUnless('en' in languages)
        self.failUnless('es' in languages)

    def test_mls_registry_agency_id(self):
        """Test for the 'agency_id' key and the default value."""
        registry = getUtility(IRegistry)
        key = 'plone.mls.core.interfaces.IMLSSettings.agency_id'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, u'cccbr')

    def test_mls_registry_mls_key(self):
        """Test for the 'mls_key' key and the default value."""
        registry = getUtility(IRegistry)
        key = 'plone.mls.core.interfaces.IMLSSettings.mls_key'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value,
                          u'IULtjlczY6l5zHZLi6jbGPUUqc2jCvD93kxBbnl1ueA')

    def test_mls_registry_mls_site(self):
        """Test for the 'mls_site' key and the default value."""
        registry = getUtility(IRegistry)
        key = 'plone.mls.core.interfaces.IMLSSettings.mls_site'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value,
                          u'http://mls.mls-cr.com/')
