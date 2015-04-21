from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Mailhide
# https://developers.google.com/recaptcha/docs/mailhideapi?csw=1
# http://www.google.com/recaptcha/mailhide/apikey
try:
    SECRET = getattr(settings, "MAILMANGLE_SECRET")
    PUBLIC = getattr(settings, "MAILMANGLE_PUBLIC")
except AttributeError:
    raise ImproperlyConfigured(
            'MAILMANGLE_SECRET and/or MAILMANGLE_PUBLIC are not defined in '
            'the settings: get yours at '
            'https://www.google.com/recaptcha/mailhide/apikey')
