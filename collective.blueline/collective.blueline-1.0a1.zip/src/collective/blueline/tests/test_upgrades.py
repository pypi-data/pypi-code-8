# -*- coding: utf-8 -*-
from collective.blueline.config import PROJECTNAME
from collective.blueline.testing import INTEGRATION_TESTING
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest


class UpgradesTestCase(unittest.TestCase):

    """Ensure product upgrades work."""

    layer = INTEGRATION_TESTING
    profile = PROJECTNAME + ':default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']

    def test_latest_version(self):
        self.assertEqual(
            self.setup.getLastVersionForProfile(self.profile)[0], u'1')

    def _match(self, item, source, dest):
        source, dest = tuple([source]), tuple([dest])
        return item['source'] == source and item['dest'] == dest

    @unittest.expectedFailure  # upgrade step not registered yet
    def test_to2_available(self):
        steps = listUpgradeSteps(self.setup, self.profile, '1')
        steps = [s for s in steps if self._match(s[0], '1', '2')]
        self.assertEqual(len(steps), 1)
