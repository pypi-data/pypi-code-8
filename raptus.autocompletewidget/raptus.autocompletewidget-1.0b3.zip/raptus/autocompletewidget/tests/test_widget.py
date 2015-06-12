# -*- coding: utf-8 -*-
"""Functional tests of widgets"""

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from raptus.autocompletewidget.testing import \
    RAPTUS_AUTOCOMPLETEWIDGET_FUNCTIONAL_TESTING

import unittest


class WidgetTestCase(unittest.TestCase):
    """Tests that widgets are working properly"""

    layer = RAPTUS_AUTOCOMPLETEWIDGET_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.portal)
        self.browser.handleErrors = False

        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        # add a page, so we can test with it
        self.portal.invokeFactory('Document',
                                  'document',
                                  title='Document Test Page')

        # Authenticates the browser
        self.browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

        # Commit so that the test browser sees these changes
        import transaction
        transaction.commit()

    def base_test_content_type(self, relative_url):
        """Tests the header 'Content-Type' in response of relative_url"""
        self.browser.open('{0}/{1}'.format(self.portal_url, relative_url))
        headers = self.browser.headers
        self.assertIn('Content-Type', headers)
        ct = self.browser.headers['Content-Type']
        self.assertEqual(ct, 'text/plain')

    def test_content_type_populate(self):
        """Tests the header 'Content-Type' in calls of
        view autocompletewidget-populate"""
        self.base_test_content_type(
            'document/@@autocompletewidget-populate?f=title&q=')

        # Inexistent field
        self.base_test_content_type(
            'document/@@autocompletewidget-populate?f=x&q=x')

    def test_content_type_search(self):
        """Tests the header 'Content-Type' in calls of
        view autocompletewidget-search"""
        self.base_test_content_type(
            'document/@@autocompletewidget-search?f=title&q=')

        # Inexistent field
        self.base_test_content_type(
            'document/@@autocompletewidget-search?f=x&q=x')
