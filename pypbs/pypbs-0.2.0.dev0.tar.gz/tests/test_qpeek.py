from . import unittest

import mock

from pypbs import qpeek

class TestBase(unittest.TestCase):
    ''' Patch get_qstat_xml '''
    def setUp(self):
        self.patch_xml = mock.patch('pypbs.qpeek.qstat.util.pbs_command')
        self.mock_xml = self.patch_xml.start()
        self.addCleanup(self.patch_xml.stop)

@mock.patch('pypbs.qpeek.sh')
class TestMain(TestBase):
    def setUp(self):
        super(TestMain,self).setUp()
        self.patch_args = mock.patch('pypbs.qpeek.parse_args')
        self.mock_args = self.patch_args.start()
        self.addCleanup(self.patch_args.stop)
        self.args = mock.Mock()
        self.mock_args.return_value = self.args
        self.mock_xml.return_value = '<Data><Job>' \
            '<Job_Id>1.host.example.com</Job_Id>' \
            '<exec_host>host2.example.com/0,2-4</exec_host>' \
            '<job_state>R</job_state>' \
            '<Join_Path>n</Join_Path>' \
            '</Job></Data>'\

    def test_calls_correct_protocol_command(self, mock_sh):
        self.args.protocol = 'ssh'
        self.args.operation = 'cat'
        self.args.jobid = ['1']
        self.args.spooldir = '/path/spool'
        qpeek.main()
        mock_sh.ssh.assert_called_once_with(
            'host2.example.com',
            'cat',
            '/path/spool/1.host.example.com.*',
            _iter=True
        )

    def test_calls_correct_operation(self, mock_sh):
        self.args.protocol = 'ssh'
        self.args.operation = 'follow'
        self.args.jobid = ['1']
        self.args.spooldir = '/path/spool'
        qpeek.main()
        mock_sh.ssh.assert_called_once_with(
            'host2.example.com',
            'tail -f',
            '/path/spool/1.host.example.com.*',
            _iter=True
        )

    def test_only_runs_jobs_state_R_job(self, mock_sh):
        self.args.protocol = 'ssh'
        self.args.operation = 'cat'
        self.args.jobid = ['1']
        self.args.spooldir = '/path/spool'
        self.mock_xml.return_value = \
            self.mock_xml.return_value.replace('>R<','>Q<')
        qpeek.main()
        self.assertEqual(0, mock_sh.ssh.call_count)
