import socket

try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode

from django.forms import Field, ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from sweetcaptcha.client import check
from sweetcaptcha.widgets import SweetCaptcha


class SweetCaptchaField(Field):

    default_error_messages = {
        'captcha_invalid': _('Invalid captcha answer, please try again.'),
        'captcha_error': _('Connection error, please try again.'),
    }

    def __init__(self, app_id=None, app_key=None, *args, **kwargs):

        self.app_id = app_id if app_id else \
            settings.SWEETCAPTCHA_APP_ID
        self.app_key = app_key if app_key else \
            settings.SWEETCAPTCHA_APP_KEY

        self.widget = SweetCaptcha(self.app_id, self.app_key)
        self.required = True
        super(SweetCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(SweetCaptchaField, self).clean(values[1])
        sckey_value = smart_unicode(values[0])
        scvalue_value = smart_unicode(values[1])

        if scvalue_value == '0':
            raise ValidationError(
                self.error_messages['required']
            )

        try:
            valid = check(self.app_id, self.app_key, sckey_value, scvalue_value)
        except socket.error:  # Catch timeouts, etc
            raise ValidationError(
                self.default_error_messages['captcha_error']
            )

        if not valid:
            raise ValidationError(
                self.default_error_messages['captcha_invalid']
            )
        return values[0]
