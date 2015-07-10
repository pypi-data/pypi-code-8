from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase as ztc
from zope.testing import doctest

import sd.analytics
import unittest


ptc.setupPloneSite(products=['collective.dancing'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             sd.analytics)
            fiveconfigure.debug_mode = False
            ztc.installPackage('collective.dancing')

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        # doctestunit.DocFileSuite(
        #    'README.txt', package='sd.analytics',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        # doctestunit.DocTestSuite(
        #    module='sd.analytics.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        # ztc.ZopeDocFileSuite(
        #    'README.txt', package='sd.analytics',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'browser.txt', package='sd.analytics',
            test_class=TestCase),

        doctest.DocFileSuite('transform.txt'),

        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
