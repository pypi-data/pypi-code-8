import unittest
from pyramid import testing


class TestAnnotationViewMapper(unittest.TestCase):
    def _get_target(self):
        from rebecca.annotationmapper.mappers import AnnotationViewMapper
        return AnnotationViewMapper

    def _make_one(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        def dummy_view(context, request, x: DummyAnnotation):
            return x

        target = self._make_one()
        result = target(dummy_view)
        request = testing.DummyRequest()
        context = testing.DummyResource()
        self.assertEqual(result(context, request), 'x')

    def test_named_annotation(self):
        def dummy_view(context, request, x: DummyAnnotation = 'dummy name'):
            return x

        target = self._make_one()
        result = target(dummy_view)
        request = testing.DummyRequest()
        context = testing.DummyResource()
        self.assertEqual(result(context, request), 'dummy name')


class DummyAnnotation(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, request):
        return self.name