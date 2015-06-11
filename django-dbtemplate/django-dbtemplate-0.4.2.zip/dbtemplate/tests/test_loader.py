from django.test import TestCase
from django.template import TemplateDoesNotExist
from mixer.backend.django import mixer
from dbtemplate.loader import DatabaseLoader


class LoaderTestCase(TestCase):

    def setUp(self):
        self.loader = DatabaseLoader(None)

    def test_load_ok(self):
        mixer.blend(
            'dbtemplate.Template',
            slug='wow.html',
            data='Hello {{ username }}!'
        )
        data, name = self.loader.load_template_source('wow.html')
        self.assertEqual(name, 'dbtemplate:wow.html')
        self.assertEqual(data, 'Hello {{ username }}!')

    def test_load_not_found(self):
        with self.assertRaises(TemplateDoesNotExist):
            self.loader.load_template_source('doesntexist.html')
