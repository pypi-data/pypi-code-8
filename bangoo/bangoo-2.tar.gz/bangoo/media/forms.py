from django import forms
from .models import Image
from crispy_forms.helper import FormHelper


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = []

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(UploadImageForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ''
        #self.fields['file'].widget = widgets.AjaxFileInput(widget_attrs={'url': reverse('media-image-upload')})
        self.fields['tags'].required = False
