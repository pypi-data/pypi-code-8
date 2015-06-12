from . import unittest

import mock

from pypbs import qstat, util

@mock.patch('pypbs.qstat.util.pbs_command')
class TestGetQstatXml(unittest.TestCase):
    def test_returns_xml_tree(self, mock_pbs_command):
        mock_pbs_command.return_value = '<Data><Job><Job_Id>1.host.example.' \
            'com</Job_Id></Job></Data>'
        self.assertEqual('Data', qstat.get_qstat_xml().tag)
