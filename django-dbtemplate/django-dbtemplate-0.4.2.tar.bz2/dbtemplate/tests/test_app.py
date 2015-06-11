from mixer.backend.django import mixer
from django.test import TestCase
from django.test.utils import override_settings

CACHED_LOADER_CONFIG = (
    ('django.template.loaders.cached.Loader', [
        'dbtemplate.loader.DatabaseLoader',
    ]),
)


@override_settings(
    ROOT_URLCONF='dbtemplate.tests.app.urls',
)
class GetTestContextTestCase(TestCase):

    def test_loader_works(self):
        mixer.blend('dbtemplate.Template',
                    slug='test.html', data='<h1>hello</h1>')
        response = self.client.get('/')
        self.assertEqual(response.content, b'<h1>hello</h1>')

    @override_settings(TEMPLATE_LOADERS=CACHED_LOADER_CONFIG)
    def test_change_template_with_cached_loader_works(self):
        template = mixer.blend('dbtemplate.Template',
                               slug='test.html', data='<h1>hello</h1>')
        self.client.get('/')
        template.data = "<h2>Bye</h2>"
        template.save()
        response = self.client.get('/')
        self.assertEqual(response.content, b'<h2>Bye</h2>')
