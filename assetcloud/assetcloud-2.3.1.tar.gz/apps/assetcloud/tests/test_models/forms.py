from django.forms.models import ModelForm
from django import forms
from django.forms.widgets import Textarea
from assetcloud.tests.test_models.models import AnotherTestAssetMetadataModel


class ExtensionModelForm(ModelForm):

    extra_field_not_in_model = forms.CharField(max_length=100, label="My Custom Label")

    class Meta:
        model = AnotherTestAssetMetadataModel

        widgets = {
            "another_required_field": Textarea(attrs={'cols': 10, 'rows': 2}),
        }
