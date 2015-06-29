""" Doc tests
"""
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from base import FacetedFunctionalTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    return unittest.TestSuite((
            Suite('README.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.faceted.tool',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/browser.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.faceted.tool',
                  test_class=FacetedFunctionalTestCase),
            Suite('docs/storage.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.faceted.tool',
                  test_class=FacetedFunctionalTestCase),
            Suite('docs/vocabularies.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.faceted.tool',
                  test_class=FacetedFunctionalTestCase),
            Suite('docs/search.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.faceted.tool',
                  test_class=FacetedFunctionalTestCase),
            Suite('docs/exportimport.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.faceted.tool',
                  test_class=FacetedFunctionalTestCase),
    ))
