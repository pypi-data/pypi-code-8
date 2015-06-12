from . import unittest
import mock

from pypbs import util

class TestParseHost(unittest.TestCase):
    def test_parses_no_host_returns_empty_list(self):
        host = ''
        self.assertEqual(('',[]), util.parse_host(host))

    def test_parses_host_no_cpu(self):
        host = 'host.example.com'
        self.assertEqual(('host.example.com',[]), util.parse_host(host))

    def test_parses_single_cpu(self):
        host = 'host.example.com/2'
        self.assertEqual(('host.example.com',[2]), util.parse_host(host))

    def test_parses_range_single_cpu(self):
        host = 'host.example.com/0,2-4'
        self.assertEqual(('host.example.com',[0,2,3,4]), util.parse_host(host))

    def test_parses_range_multi_cpu_list(self):
        host = 'host.example.com/0,2'
        self.assertEqual(('host.example.com',[0,2]), util.parse_host(host))

class TestParseRangestring(unittest.TestCase):
    def test_parses_empty_string_returns_empty_list(self):
        self.assertEqual([], util.parse_rangestring(''))

    def test_parses_dash_range(self):
        self.assertEqual([1,2,3,4], util.parse_rangestring('1-4'))
    
    def test_parses_multi_range(self):
        self.assertEqual([1,3,5], util.parse_rangestring('1,3,5'))

    def test_parses_complex_rangestring(self):
        self.assertEqual([0,1,2,3,5,7,8,9], util.parse_rangestring('0-3,5,7-9'))

@mock.patch('pypbs.util.sh')
class TestPBSCommand(unittest.TestCase):
    def test_returns_parsed_xml_output(self, mock_sh):
        mock_sh.foo.return_value = '<Data></Data>'
        r = util.pbs_command('foo', 'bar', baz=True)
        self.assertEqual('<Data></Data>', r)
        mock_sh.foo.assert_called_once_with('bar', baz=True)

@mock.patch('pypbs.util.sh')
class TestPBSXmlCommand(unittest.TestCase):
    def test_ensures_x_argument_for_command(self, mock_sh):
        mock_sh.foo.return_value = '<Data></Data>'
        r = util.pbs_xml_command('foo', 'bar', baz=True)
        self.assertEqual('<Data></Data>', r)
        mock_sh.foo.assert_called_once_with('bar', baz=True, x=True)

    def test_ensures_x_argument_for_command(self, mock_sh):
        mock_sh.foo.return_value = '<Data></Data>'
        r = util.pbs_xml_command('foo', 'bar', baz=True)
        self.assertEqual('Data', r.tag)
        mock_sh.foo.assert_called_once_with('bar', baz=True, x=True)
