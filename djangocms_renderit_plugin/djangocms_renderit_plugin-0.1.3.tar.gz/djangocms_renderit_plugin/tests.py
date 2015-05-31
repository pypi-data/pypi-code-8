from django.test import TestCase, override_settings
from cms.plugin_rendering import PluginContext
from cms.api import add_plugin
from cms.models import Placeholder
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from .cms_plugins import RenderItPlugin


# noinspection PyUnusedLocal
def sample_context_processor(instance, placeholder, context):
    return {
        'dummy_var': 'whatzaaap!',
    }

CMS_PLUGIN_CONTEXT_PROCESSORS = (
    'apps.djangocms_renderit_plugin.tests.sample_context_processor',
)


class RenderitPluginTests(TestCase):

    def test_empty_plugin(self):
        placeholder = Placeholder.objects.create()
        model_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        html = model_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=model_instance,
            placeholder=placeholder,
        ))
        self.assertEqual('', html)

    def test_simple_text_plugin(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='just some text',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertEqual('just some text', html.strip())

    def test_text_plugin_with_url(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='admin: {% url "admin:index" %}',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertEqual('admin: /en/admin/', html.strip())

    @override_settings(CMS_RENDERIT_TAG_LIBRARIES=('sample_tags', ))
    def test_text_plugin_with_custom_tag_in_settings(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='sample: {% sample %}',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertIn('HERE BE DA SIMPLE TAG!', html)

    @override_settings(CMS_RENDERIT_TAG_LIBRARIES=())
    def test_text_plugin_with_custom_tag_on_model(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
            tag_libraries='sample_tags',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='sample: {% sample %}',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertIn('HERE BE DA SIMPLE TAG!', html)

    @override_settings(CMS_PLUGIN_CONTEXT_PROCESSORS=CMS_PLUGIN_CONTEXT_PROCESSORS)
    def test_text_plugin_with_custom_tag_on_model(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
            tag_libraries='sample_tags',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='dummy_var: {{ dummy_var }}',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertIn('whatzaaap!', html)
