import sys
import unittest

from pyramid import testing
from pyramid.compat import text_type

class Base(object):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _getTemplatePath(self, name):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(here, 'fixtures', name)

class Test_renderer_factory(Base, unittest.TestCase):
    def _callFUT(self, info):
        from pyramid_pystache.mustache import renderer_factory
        return renderer_factory(info)

    def test_it(self):
        # this test is way too functional
        from pyramid_pystache.mustache import MustacheTemplateRenderer
        info = DummyInfo()
        result = self._callFUT(info)
        self.assertEqual(result.__class__, MustacheTemplateRenderer)

class MustacheTemplateRendererTests(Base, unittest.TestCase):
    def _getTargetClass(self):
        from pyramid_pystache.mustache import MustacheTemplateRenderer
        return MustacheTemplateRenderer

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def test_instance_implements_ITemplateRenderer(self):
        from zope.interface.verify import verifyObject
        from pyramid_pystache.interfaces import ITemplateRenderer
        path = self._getTemplatePath('minimal.mustache')
        lookup = DummyLookup()
        verifyObject(ITemplateRenderer, self._makeOne(path, lookup))

    def test_class_implements_ITemplateRenderer(self):
        from zope.interface.verify import verifyClass
        from pyramid_pystache.interfaces import ITemplateRenderer
        verifyClass(ITemplateRenderer, self._getTargetClass())

    def test_call(self):
        minimal = self._getTemplatePath('minimal.mustache')
        lookup = DummyLookup()
        instance = self._makeOne(minimal, lookup)
        result = instance({}, {})
        self.assertTrue(isinstance(result, text_type))
        self.assertEqual(result.rstrip('\n'),
                     'Hello.')

    def test_call_with_value(self):
        nonminimal = self._getTemplatePath('nonminimal.mustache')
        lookup = DummyLookup()
        instance = self._makeOne(nonminimal, lookup)
        result = instance({'name': 'test'}, {})
        self.assertEqual(result.rstrip('\n'),
                'Hello, test!')

    def test_call_with_partial(self):
        nonminimal = self._getTemplatePath('partial.mustache')
        lookup = DummyLookup()
        instance = self._makeOne(nonminimal, lookup)
        result = instance({'name': 'test'}, {})
        self.assertEqual(result.rstrip('\n'),
                '<div>\n    Hello, test!\n</div>')

    def test_template_reified(self):
        minimal = self._getTemplatePath('minimal.mustache')
        lookup = DummyLookup()
        instance = self._makeOne(minimal, lookup)
        self.assertFalse('template' in instance.__dict__)
        template  = instance.template
        self.assertEqual(template, instance.__dict__['template'])

    def test_call_with_nondict_value(self):
        minimal = self._getTemplatePath('minimal.mustache')
        lookup = DummyLookup()
        instance = self._makeOne(minimal, lookup)
        self.assertRaises(ValueError, instance, None, {})

    def test_implementation(self):
        minimal = self._getTemplatePath('minimal.mustache')
        lookup = DummyLookup()
        instance = self._makeOne(minimal, lookup)
        result = instance.implementation()()
        self.assertTrue(isinstance(result, text_type))
        self.assertEqual(result.rstrip('\n'),
                     'Hello.')


class DummyLookup(object):
    pass

class DummyRegistry(object):
    def queryUtility(self, iface, name):
        self.queried = iface, name
        return None

    def registerUtility(self, impl, iface, name):
        self.registered = impl, iface, name

class DummyInfo(object):
    def __init__(self):
        self.registry = DummyRegistry()
        self.type = '.mustache'
        self.name = 'fixtures/minimal.mustache'
        self.package = sys.modules[__name__]
        self.settings = {}

