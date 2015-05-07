# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.core.exceptions import ValidationError
from assetcloud.forms import AssetForm
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.unit.utils import OverrideAssetcloudSettings

from .utils import UnitTestCase

from assetcloud.templatetags.renderform import render_form, render_field, render_asset_form
from django import forms
from django.forms import widgets
from django.template import Context


class TestForm(forms.Form):
    test = forms.CharField(required=True)


class HiddenFieldForm(forms.Form):
    hidden = forms.CharField(required=True, widget=widgets.HiddenInput())


def always_fail_with_message_that_needs_escaping(value):
    raise ValidationError('This should <really> be escaped')


class HiddenFieldErrorNeedsEscapingForm(forms.Form):
    hidden = forms.CharField(required=False, widget=widgets.HiddenInput(),
                             validators=[always_fail_with_message_that_needs_escaping])


class RenderFormTests(UnitTestCase):
    def test_render_form_renders_form(self):
        output = render_form(Context(), TestForm())
        self.assertIn("input", output)
        self.assertIn('type="text"', output)

    def test_render_form_applies_class(self):
        output = render_form(Context(), TestForm(), "test-class")
        self.assertIn('class="test-class"', output)

    def test_render_form_marks_required(self):
        output = render_form(Context(), TestForm(), mark_required=True)
        self.assertIn('<strong>*</strong>', output)

    def test_no_label_for_hidden_fields(self):
        output = render_field(Context(), HiddenFieldForm()['hidden'])
        self.assertNotIn('</label>', output)

    def test_no_label_for_hidden_fields_in_form(self):
        output = render_form(Context(), HiddenFieldForm())
        self.assertNotIn('</label>', output)

    def test_hidden_field_errors_included_in_form(self):
        bound_form = HiddenFieldForm(data={'hidden': ''})
        output = render_form(Context(), bound_form)
        self.assertIn('This field is required', output)

    def test_hidden_field_errors_escaped(self):
        bound_form = HiddenFieldErrorNeedsEscapingForm(data={'hidden': 'something'})
        output = render_form(Context(), bound_form)
        self.assertIn('This should &lt;really&gt; be escaped', output)

    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    @TNABotContractTest
    def test_render_asset_form_renders_the_form_with_extension(self):
        form = AssetForm()
        output = render_asset_form(Context(), form)
        self.assertIn("id_required_field", output)
        self.assertIn("id_non_required_field", output)

    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[
        "test_models.TestAssetMetadataModel",
        "test_models.AnotherTestAssetMetadataModel"
    ])
    def test_render_asset_form_renders_the_form_with_more_than_one_extension(self):
        form = AssetForm()
        output = render_asset_form(Context(), form)
        self.assertIn("id_required_field", output)
        self.assertIn("id_non_required_field", output)
        self.assertIn("id_another_required_field", output)
        self.assertIn("id_another_non_required_field", output)

    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[])
    def test_render_asset_form_renders_the_form_with__no_extension(self):
        form = AssetForm()
        output = render_asset_form(Context(), form)
        self.assertNotIn("id_required_field", output)
        self.assertNotIn("id_non_required_field", output)
        self.assertNotIn("id_another_required_field", output)
        self.assertNotIn("id_another_non_required_field", output)

    @OverrideAssetcloudSettings(
        ASSET_METADATA_MODELS=[
            "test_models.TestAssetMetadataModel",
            (
                "test_models.AnotherTestAssetMetadataModel",
                "assetcloud.tests.test_models.forms.ExtensionModelForm"
            )
        ]
    )
    @TNABotContractTest
    def test_render_asset_form_renders_custom_model_form_extra_fields(self):
        form = AssetForm()
        output = render_asset_form(Context(), form)
        self.assertIn("id_required_field", output)
        self.assertIn("id_non_required_field", output)
        self.assertIn("id_another_required_field", output)
        self.assertIn("id_another_non_required_field", output)
        self.assertIn("id_extra_field_not_in_model", output)

    @OverrideAssetcloudSettings(
        ASSET_METADATA_MODELS=[
            "test_models.TestAssetMetadataModel",
            (
                "test_models.AnotherTestAssetMetadataModel",
                "assetcloud.tests.test_models.forms.ExtensionModelForm"
            )
        ]
    )
    @TNABotContractTest
    def test_render_asset_form_renders_custom_model_form_widgets(self):
        form = AssetForm()
        output = render_asset_form(Context(), form)
        self.assertIn("id_required_field", output)
        self.assertIn("id_non_required_field", output)
        self.assertIn("<textarea cols=\"10\" id=\"id_another_required_field\" name=\"another_required_field\" rows=\"2\">", output)
        self.assertIn("id_another_non_required_field", output)
        self.assertIn("id_extra_field_not_in_model", output)
