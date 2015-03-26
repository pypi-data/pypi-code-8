from cement.core import controller, foundation, backend, handler
from cement.utils import test
from common.testutils import decallmethods
from droopescan import DroopeScan
from lxml import etree
from mock import patch, MagicMock
from plugins.drupal import Drupal
from plugins import Scan
import responses

class MockHash():
    files = None
    def mock_func(self, *args, **kwargs):
        url = kwargs['file_url']
        try:
            return self.files[url]
        except KeyError:
            raise RuntimeError(url)

class BaseTest(test.CementTestCase):
    app_class = DroopeScan
    scanner = None

    base_url = "http://adhwuiaihduhaknbacnckajcwnncwkakncw.com/"
    base_url_https = "https://adhwuiaihduhaknbacnckajcwnncwkakncw.com/"
    valid_file = 'tests/resources/url_file_valid.txt'

    param_base = ["--url", base_url, '-n', '10']
    param_plugins = param_base + ["-e", 'p']
    param_interesting = param_base + ["-e", 'i']
    param_themes = param_base + ["-e", 't']
    param_version = param_base + ["-e", 'v']
    param_all = param_base + ["-e", 'a']

    versions_xsd = 'common/versions.xsd'
    xml_file = 'tests/resources/versions.xml'

    def setUp(self):
        super(BaseTest, self).setUp()
        self.reset_backend()
        self.app = DroopeScan(argv=[],
            plugin_config_dir="./plugins.d",
            plugin_dir="./plugins")
        handler.register(Scan)
        self.app.testing = True
        self.app.setup()
        responses.add(responses.HEAD, self.base_url, status=200)

    def _init_scanner(self):
        self.scanner = Drupal()
        self.scanner._general_init()

    def tearDown(self):
        self.app.close()

    def mock_controller(self, plugin_label, method, return_value = None,
            side_effect = None, mock = None):
        """
            Mocks controller by label. Can only be used to test controllers
            that get instantiated automatically by cement.
            @param plugin_label e.g. 'drupal'
            @param method e.g. 'enumerate_plugins'
            @param return_value what to return. Default is None, unless the
                method starts with enumerate_*, in which case the result is a
                tuple as expected by BasePlugin.
            @param mock the MagicMock to place. If None, a blank MagicMock is
                created.
            @param side_effect if set to an exception, it will raise an
                exception.
        """
        if mock:
            m = mock
        else:
            m = MagicMock()

        if return_value != None:
            m.return_value = return_value
        else:
            if method.startswith("enumerate_"):
                m.return_value = ({"a":[]}, True)

        if side_effect:
            m.side_effect = side_effect

        setattr(self.controller_get(plugin_label), method, m)
        return m

    def controller_get(self, plugin_label):
        return backend.__handlers__['controller'][plugin_label]

    def add_argv(self, argv):
        """
            Concatenates list with self.app.argv.
        """
        self.app._meta.argv += argv

    def assert_called_contains(self, mocked_method, kwarg_name, kwarg_value):
        """
            Assert kwarg_name equals kwarg name in call to mocked_method.
            @param mocked_method mock to check the call to.
            @param kwarg_name name of the param. E.g. 'url'
            @param kwarg_value expected value. E.g. 'https://www.drupal.org/'
        """
        args, kwargs = mocked_method.call_args
        assert kwargs[kwarg_name] == kwarg_value, "Parameter is not as expected."

    def assert_called_contains_all(self, mocked_method, kwarg_name, kwarg_value):
        call_list = mocked_method.call_args_list
        if len(mocked_method.call_args_list) == 0:
            assert False, "No calls to mocked method"

        for args, kwargs in call_list:
            assert kwargs[kwarg_name] == kwarg_value

    def assert_args_contains(self, mocked_method, position, expected_value):
        """
            Assert that the call contains this argument in the args at position position.
        """
        args, kwargs = mocked_method.call_args
        assert args[position] == expected_value

    def respond_several(self, base_url, data_obj, verb=responses.HEAD, headers=[]):
        for status_code in data_obj:
            for item in data_obj[status_code]:
                url = base_url % item
                responses.add(verb, url,
                        body=str(status_code), status=status_code,
                        adding_headers=headers)

    def mock_all_enumerate(self, plugin_name):
        all = []
        all.append(self.mock_controller(plugin_name, 'enumerate_plugins'))
        all.append(self.mock_controller(plugin_name, 'enumerate_themes'))
        all.append(self.mock_controller(plugin_name, 'enumerate_interesting'))
        all.append(self.mock_controller(plugin_name, 'enumerate_version'))

        for a in all:
            all[a].return_value = ([], True)

        return all

    def mock_all_url_file(self, url_file):
        with open(url_file) as f:
            for url in f:
                url_tpl = url.strip('\n') + '%s'

                self.respond_several(url_tpl, {
                    403: [Drupal.forbidden_url],
                    200: ['', 'misc/drupal.js'],
                    404: [self.scanner.not_found_url]
                })

    def mock_xml(self, xml_file, version_to_mock):
        '''
            Generates all mock data, and returns a MagicMock which can be used
            to replace self.scanner.enumerate_file_hash.

            @param xml_file a file, which contains the XML to mock.
            @param version_to_mock the version which we will pretend to be.
            @return a function which can be used to mock
                BasePlugin.enumerate_file_hash

            @usage self.scanner.enumerate_file_hash = self.mock_xml(self.xml_file, "7.27")
        '''
        with open(xml_file) as f:
            doc = etree.fromstring(f.read())
            files_xml = doc.xpath('//cms/files/file')

            files = {}
            for file in files_xml:
                url = file.get('url')
                versions = file.xpath('version')
                for file_version in versions:
                    version_number = file_version.get('nb')
                    md5 = file_version.get('md5')

                    if version_number == version_to_mock:
                        files[url] = md5

                if not url in files:
                    files[url] = '5d41402abc4b2a76b9719d911017c592'

            ch_xml_all = doc.findall('./files/changelog')
            if len(ch_xml_all) > 0:
                for ch_xml in ch_xml_all:
                    ch_url = ch_xml.get('url')
                    ch_versions = ch_xml.findall('./version')
                    found = False
                    for ch_version in ch_versions:
                        ch_nb = ch_version.get('nb')
                        if ch_nb == version_to_mock:
                            files[ch_url] = ch_version.get('md5')
                            found = True

        mock_hash = MockHash()
        mock_hash.files = files
        mock = MagicMock(side_effect=mock_hash.mock_func)

        return mock

