import json
import six
from django.test import TestCase as DjTestCase


def loadJson(msg):
    """Read json from bytes or unicode message"""
    if isinstance(msg, six.binary_type):
        msg = six.text_type(msg, encoding='utf-8')
    return json.loads(msg)


class TestCase(DjTestCase):
    """Wrapper to handle bytestrings in JSON assertions"""

    def assertJSONEqual(self, raw, expected, msg=None):
        if isinstance(raw, six.binary_type):
            raw = six.text_type(raw, encoding='utf-8')
        super(TestCase, self).assertJSONEqual(raw, expected, msg)

    def assertJSONNotEqual(self, raw, expected, msg=None):
        if isinstance(raw, six.binary_type):
            raw = six.text_type(raw, encoding='utf-8')
        super(TestCase, self).assertJSONNotEqual(raw, expected, msg)
