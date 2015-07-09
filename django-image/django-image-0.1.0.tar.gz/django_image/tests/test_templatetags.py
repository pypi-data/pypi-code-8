from unittest import TestCase
from django.template import Context
from django.template import Template


class DummyFile(object):
    def __init__(self, url='http://example.com/static/hello.jpg'):
        self.url = url


class TemplateTagsTestCase(TestCase):

    def render_template(self, string, **context):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_image(self):
        rendered = self.render_template(
            '{% load images %}'
            '{% image img width=100 height=60 _alt="Hello" %}',
            img=DummyFile(),
        )
        self.assertEqual(
            rendered,
            '<img src="http://imgservice.com/api/http://example.com/static/hello.jpg?height=60&width=100" alt="Hello">'
        )

    def test_imageas(self):
        rendered = self.render_template(
            '{% load images %}'
            '{% imageas img width=100 height=60 _alt="Hello" as myimage %}'
            '{{ myimage|safe }}',
            img=DummyFile(),
        )
        self.assertEqual(
            rendered,
            '<img src="http://imgservice.com/api/http://example.com/static/hello.jpg?height=60&width=100" alt="Hello">'
        )

    def test_imageurl(self):
        rendered = self.render_template(
            '{% load images %}'
            '{% imageurl img width=100 height=60 _alt="Hello" %}',
            img=DummyFile(),
        )
        self.assertEqual(
            rendered,
            'http://imgservice.com/api/http://example.com/static/hello.jpg?height=60&width=100'
        )

    def test_imageurlas(self):
        rendered = self.render_template(
            '{% load images %}'
            '{% imageurlas img width=100 height=60 _alt="Hello" as url %}'
            '{{ url|safe }}',
            img=DummyFile(),
        )
        self.assertEqual(
            rendered,
            'http://imgservice.com/api/http://example.com/static/hello.jpg?height=60&width=100'
        )
