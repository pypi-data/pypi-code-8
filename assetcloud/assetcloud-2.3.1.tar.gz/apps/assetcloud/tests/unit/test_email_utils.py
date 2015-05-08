from django.template import loader
from django.template.context import Context
from django.test.testcases import TestCase
from assetcloud.mail import _render_node
from assetcloud.tests.contract.utils import TNABotContractTest


class EmailUtilTests(TestCase):

    template_name = "test_models/emails/test.html"

    def setUp(self):
        super(EmailUtilTests, self).setUp()
        self.template = loader.get_template(self.template_name)
        self.context = Context()

    @TNABotContractTest
    def test_block_renderer_can_render_extended_blocks(self):
        subject_text = "The best subject"

        self.context.update(
            {
                "subject": subject_text
            }
        )

        rendered_block = _render_node(
            self.template,
            "subject",
            self.context
        )

        self.assertEqual(rendered_block, subject_text)

    @TNABotContractTest
    def test_block_renderer_renders_parent_content(self):
        subject_text = "The best subject"
        body_html = "Body HTML"
        body_plain = "Body Plain"

        self.context.update(
            {
                "subject": subject_text,
                "html_content": body_html,
                "plain_content": body_plain
            }
        )

        rendered_html_block = _render_node(self.template, "html", self.context)
        rendered_plain_block = _render_node(self.template, "plain", self.context)

        self.assertEqual("WRAPPER >>Body HTML<<", rendered_html_block)
        self.assertEqual("TEXT WRAPPER >>Body Plain<<", rendered_plain_block)
