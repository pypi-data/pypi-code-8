from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from sweetcaptcha.client import get_html


class SweetCaptcha(forms.widgets.Widget):

    sckey_name = 'sckey'
    scvalue = 'scvalue'

    def __init__(self, app_id=None, app_key=None, attrs={}, *args,
                 **kwargs):
        self.app_id = app_id if app_id else \
            settings.SWEETCAPTCHA_APP_ID
        self.app_key = app_key if app_key else \
            settings.SWEETCAPTCHA_APP_KEY

        super(SweetCaptcha, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % get_html(self.app_id, self.app_key))

    def value_from_datadict(self, data, files, name):
        return [
            data.get(self.sckey_name, None),
            data.get(self.scvalue, None)
        ]
