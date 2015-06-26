# -*- coding: utf-8 -*-

import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

from Products.CMFCore.utils import getToolByName

ptc.setupPloneSite()

import c2.search.kananormalizer

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             c2.search.kananormalizer)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


class TestCanUseSpritter(TestCase):
    """Can Replace the catalog """
    def afterSetUp(self):
        pass

    def testWordNormalizer(self):
        from Products.ZCTextIndex.PipelineFactory import element_factory

        group = 'Case Normalizer'
        names = element_factory.getFactoryNames(group)
        self.failUnless('Unicode Ignoring Accents Case Normalizer with Japanese Kana Normalizer' in names)


class TestSearchingJapanese(TestCase):
    """ Install Japanese test """
    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('c2.search.kananormalizer')
        self.setRoles(('Manager',))
        self.portal.invokeFactory('Document', 'doc1')
        self.doc1 = getattr(self.portal, 'doc1')
        self.doc1.setTitle("Ploneは素晴らしい。")
        self.doc1.setText("このページは予想している通り、テストです。 Pages Testing. アクセスして")
        self.doc1.reindexObject()

    def testSearch(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        items1 = catalog(SearchableText="予想")
        self.assertEqual(len(items1), 1)
        items12 = catalog(SearchableText="素晴らしい")
        self.assertEqual(len(items12), 1)
        items13 = catalog(SearchableText="Pages")
        self.assertEqual(len(items13), 1)
        items14 = catalog(SearchableText="ページ")
        self.assertEqual(len(items14), 1)
        items15 = catalog(SearchableText="予想*")
        self.assertEqual(len(items15), 1)
        items16 = catalog(SearchableText=u"予想")
        self.assertEqual(len(items16), 1)
        items17 = catalog(SearchableText="予想　テスト") # And search by Full width space
        self.assertEqual(len(items17), 1)

        items21 = catalog(SearchableText="あくせす") # Kana test
        self.assertEqual(len(items21), 1)
        items22 = catalog(SearchableText="シテイル") # Kana test
        self.assertEqual(len(items22), 1)
        items23 = catalog(SearchableText="すし") # Kana test
        self.assertEqual(len(items23), 1)

        self.portal.manage_delObjects(['doc1'])
        items2 = catalog(SearchableText="予想")
        self.assertEqual(len(items2), 0)

def test_suite():
    return unittest.TestSuite([

        unittest.makeSuite(TestCanUseSpritter),
        unittest.makeSuite(TestSearchingJapanese),


        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='c2.search.kananormalizer',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='c2.search.kananormalizer.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='c2.search.kananormalizer',
        #    test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='c2.search.kananormalizer',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
