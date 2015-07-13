from unittest import TestCase
import mock
from .plugin import ESLint


class ESLintTest(TestCase):
    def test_command_returns_airbnb_if_no_config(self):
        plugin = ESLint(None)
        with mock.patch('os.path') as mock_op:
            mock_op.join.return_value = '/tmp/foo.js'
            mock_op.exists.return_value = False
            cmd = plugin.get_command('/tmp')
            self.assertEqual('eslint -f compact', cmd)

    def test_command_returns_config_if_available(self):
        plugin = ESLint(None)
        with mock.patch('os.path') as mock_op:
            path = '/tmp/.eslintrc'
            mock_op.join.return_value = path
            mock_op.exists.return_value = True
            cmd = plugin.get_command('/tmp')

            self.assertEqual('eslint -f compact -c /tmp/.eslintrc', cmd)
