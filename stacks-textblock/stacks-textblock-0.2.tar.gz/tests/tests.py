from __future__ import unicode_literals
import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stacks_textblock.models import StacksTextBlock, StacksTextBlockList


class StacksTextBlockTestCase(TestCase):
    """The test suite for stacks-page"""

    fixtures = ['stackstextblock.json']
    maxDiff = None

    def setUp(self):
        """Set up the test suite."""
        password = '12345'
        user = User.objects.create_user(
            username='test_user',
            email='user@test.com',
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        user_client = Client()
        user_login = user_client.login(
            username='test_user',
            password=password
        )
        self.assertTrue(user_login)
        self.user = user
        self.user_client = user_client
        self.textblock = StacksTextBlock.objects.get()
        self.textblocklist = StacksTextBlockList.objects.get()

    def test_instances(self):
        """Test the test StacksTextBlock instance."""
        self.assertEqual(
            self.textblock.__str__(),
            'Test Text Block'
        )
        self.assertEqual(
            self.textblocklist.__str__(),
            'Test Text Block List'
        )
        self.assertEqual(
            self.textblocklist
            .stackstextblocklisttextblock_set.all()[0].__str__(),
            'Test Text Block List 1. Test Text Block'
        )

    def test_serialization(self):
        """Test the StacksTextBlock textplusstuff serializer."""
        response = self.client.get(
            '/textplusstuff/stacks_textblock/stackstextblock/detail/1/'
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            json.loads(response.content)['context'],
            {
                "name": "Test Text Block",
                "display_title": "Some test text!",
                "extra_context": {},
                "content": {
                    "as_plaintext": (
                        "Here's a heading.\nAnd here's a paragraph with "
                        "some emphasized text and some boldtext.\n\n"
                        "And here's a pullquote.\n\n"
                    ),
                    "as_html": (
                        "<h1>Here's a heading.</h1>\n\n<p>And here's a "
                        "paragraph with some <em>emphasized text</em> and "
                        "some <strong>boldtext</strong>.</p>\n\n"
                        "<blockquote>\n  <p>And here's a pullquote.</p>\n"
                        "</blockquote>\n"
                    ),
                    "raw_text": (
                        "# Here's a heading.\n\nAnd here's a paragraph "
                        "with some *emphasized text* and some **boldtext**"
                        ".\n\n> And here's a pullquote."
                    ),
                    "as_html_no_tokens": (
                        "<h1>Here's a heading.</h1>\n\n<p>And here's a "
                        "paragraph with some <em>emphasized text</em> and "
                        "some <strong>boldtext</strong>.</p>\n\n"
                        "<blockquote>\n  <p>And here's a pullquote.</p>\n"
                        "</blockquote>\n"
                    ),
                    "as_markdown": (
                        "# Here's a heading.\n\nAnd here's a paragraph "
                        "with some *emphasized text* and some **boldtext**"
                        ".\n\n> And here's a pullquote."
                    )
                }
            }
        )

    def test_list_serialization(self):
        """Test the StacksTextBlockList textplusstuff serializer."""
        response = self.client.get(
            '/textplusstuff/stacks_textblock/stackstextblocklist/detail/1/'
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            json.loads(response.content)['context'],
            {
                "name": "Test Text Block List",
                "display_title": "A test list of text blocks",
                "text_blocks": [
                    {
                        "name": "Test Text Block",
                        "display_title": "Some test text!",
                        "content": {
                            "as_plaintext": (
                                "Here's a heading.\nAnd here's a paragraph "
                                "with some emphasized text and some boldtext."
                                "\n\nAnd here's a pullquote.\n\n"
                            ),
                            "as_html": (
                                "<h1>Here's a heading.</h1>\n\n"
                                "<p>And here's a paragraph with some "
                                "<em>emphasized text</em> and some <strong>"
                                "boldtext</strong>.</p>\n\n<blockquote>\n  "
                                "<p>And here's a pullquote.</p>\n"
                                "</blockquote>\n"
                            ),
                            "raw_text": (
                                "# Here's a heading.\n\nAnd here's a "
                                "paragraph with some *emphasized text* "
                                "and some **boldtext**.\n\n> And here's a "
                                "pullquote."
                            ),
                            "as_html_no_tokens": (
                                "<h1>Here's a heading.</h1>\n\n<p>And here's "
                                "a paragraph with some <em>emphasized text"
                                "</em> and some <strong>boldtext</strong>."
                                "</p>\n\n<blockquote>\n  <p>And here's a "
                                "pullquote.</p>\n</blockquote>\n"
                            ),
                            "as_markdown": (
                                "# Here's a heading.\n\nAnd here's "
                                "a paragraph with some *emphasized text* and "
                                "some **boldtext**.\n\n> And here's a "
                                "pullquote."
                            )
                        },
                        "extra_context": {}
                    }
                ],
                "extra_context": {}
            }
        )
