from django.conf import settings
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.core.urlresolvers import NoReverseMatch
from bangoo.navigation.models import Menu


@override_settings(ROOT_URLCONF='tests.urls')
class AdminUrlResolverTest(TestCase):
    def test_need_act_menu(self):
        """
        Context must have act_menu variable
        """
        context = Context()
        template = Template(
            """
                {% load navigation_tags %}
                {% admin_url 'example-view' %}
            """
        )
        self.assertRaises(NoReverseMatch, lambda: template.render(context))

    def test_generated_url(self):
        m = Menu(id=1, path='/valami/', plugin='bangoo.media')
        context = Context({'act_menu': m})
        template = Template(
            """
                {% load navigation_tags %}
                {% admin_url 'media-images-home' %}
            """
        )
        out = template.render(context).strip()
        self.assertEqual(out, '/admin/menu/%s/images/' % m.pk)