# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Custom form fields (not model fields).
"""

import assetcloud.widgets
import django.forms
import taggit.forms
import json


class EmailField(django.forms.EmailField):
    widget = assetcloud.widgets.EmailInput


class SpacesAllowedTagField(taggit.forms.TagField):
    """
    As the standard taggit behaviour, but adds a trailing comma if no
    commas are present.

    This change essentially guarantees that only commas are used so that
    tags CAN contain spaces.
    """
    def clean(self, value):
        try:
            if ',' not in value:
                value += ','
        except (AttributeError, TypeError):
            pass  # None or invalid input
        return super(SpacesAllowedTagField, self).clean(value)


class LowerCasingTagField(SpacesAllowedTagField):
    """
    As the standard taggit behaviour, but lowercases all tags.
    """
    widget = assetcloud.widgets.TagWidget

    def clean(self, value):
        tags = super(LowerCasingTagField, self).clean(value)

        return [tag.lower() for tag in tags]


class ClientsideTagField(django.forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = django.forms.widgets.HiddenInput
        kwargs['required'] = False
        super(ClientsideTagField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(ClientsideTagField, self).clean(value)
        try:
            return json.loads(value or '[]')
        except ValueError:
            raise django.forms.ValidationError('Invalid tags')
