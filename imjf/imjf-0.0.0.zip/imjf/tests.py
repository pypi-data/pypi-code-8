
import unittest

from .client import is_my_js_fucked
from .exceptions import IMJFException

class TestIntegration(unittest.TestCase):
    def url(self, test_name):
        return 'http://www.ismyjsfucked.com/tests/{name}.html'.format(name=test_name)

    def test_ok(self):
        assert is_my_js_fucked(self.url('ok')) is False

    def test_exception(self):
        assert is_my_js_fucked(self.url('exception')) is True

    def test_syntax_error(self):
        assert is_my_js_fucked(self.url('syntax-error')) is True

    def test_unknown(self):
        assert is_my_js_fucked(self.url('timeout')) is None

    def test_precedence(self):
        assert is_my_js_fucked(self.url('ok'), self.url('syntax-error'), self.url('timeout')) is True
        assert is_my_js_fucked(self.url('ok'), self.url('syntax-error')) is True
        assert is_my_js_fucked(self.url('ok'), self.url('timeout')) is None

    def test_invalid_url(self):
        with self.assertRaises(IMJFException) as context:
            is_my_js_fucked('not-a-valid-url')

        assert str(context.exception) == "Invalid URL 'not-a-valid-url'"
