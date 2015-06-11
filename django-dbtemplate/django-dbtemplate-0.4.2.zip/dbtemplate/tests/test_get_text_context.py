from mixer.backend.django import mixer
from django.test import TestCase
from dbtemplate.tryrenderer import get_test_context


class GetTestContextTestCase(TestCase):

    def test_simple_string_ok(self):
        spec = {
            "username": "hello",
        }
        result = get_test_context(spec)
        self.assertEqual(result['username'], "hello")

    def test_random_model_no_entries_ok(self):
        spec = {
            "mm": {
                "type": "model",
                "app": "app",
                "model": "TestModel",
            }
        }
        result = get_test_context(spec)
        self.assertIsNone(result['mm'])

    def test_random_model_with_entries_ok(self):
        mm = mixer.blend('app.TestModel')
        spec = {
            "mm": {
                "type": "model",
                "app": "app",
                "model": "TestModel",
            }
        }
        result = get_test_context(spec)
        self.assertEqual(result['mm'].pk, mm.pk)
