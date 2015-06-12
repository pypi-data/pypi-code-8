from . import unittest
from . import make_node_info

import mock

from pypbs import pbsstatus

class TestGetPbsnodesXML(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch('pypbs.pbsstatus.util.pbs_command')
        self.mock_pbs_command = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_gets_xml_tree(self):
        self.mock_pbs_command.return_value = '<Data></Data>'
        r = pbsstatus.get_pbsnodes_xml()
        self.assertTrue('Data', r.tag)

    def test_calls_pbsnodes_correct_with_arguments(self):
        self.mock_pbs_command.return_value = '<Data></Data>'
        r = pbsstatus.get_pbsnodes_xml(['foo','bar'])
        self.mock_pbs_command.assert_called_once_with(
            'pbsnodes', 'foo', 'bar', x=True
        )

    def test_calls_pbsnodes_correct_with_no_arguments(self):
        self.mock_pbs_command.return_value = '<Data></Data>'
        r = pbsstatus.get_pbsnodes_xml()
        self.mock_pbs_command.assert_called_once_with('pbsnodes', x=True)

class TestClusterStatus(unittest.TestCase):
    def setUp(self):
        self.nodes_info = {
            'foo': make_node_info(),
            'bar': make_node_info()
        }

    def test_has_no_jobs(self):
        del self.nodes_info['foo']['jobs']
        r = pbsstatus.cluster_info(self.nodes_info)

    def test_does_load_utilization_gt_1(self):
        self.nodes_info['foo']['status']['ncpus'] = '20'
        self.nodes_info['foo']['status']['loadave'] = '40.0'
        self.nodes_info['bar']['status']['ncpus'] = '20'
        self.nodes_info['bar']['status']['loadave'] = '40.0'
        r = pbsstatus.cluster_info(self.nodes_info)
        self.assertEqual(2.0, r['load_utilization'])

    def test_does_load_utilization_0(self):
        self.nodes_info['foo']['status']['ncpus'] = '20'
        self.nodes_info['foo']['status']['loadave'] = '0.0'
        self.nodes_info['bar']['status']['ncpus'] = '20'
        self.nodes_info['bar']['status']['loadave'] = '0.0'
        r = pbsstatus.cluster_info(self.nodes_info)
        self.assertEqual(0.0, r['load_utilization'])

    def test_does_np_utilization_1(self):
        jobs = ['0/1.foo','1-8/2.foo','9/3.foo']
        self.nodes_info['foo']['jobs'] = jobs
        self.nodes_info['bar']['jobs'] = jobs
        r = pbsstatus.cluster_info(self.nodes_info)
        self.assertEqual(20, r['total_np'])
        self.assertEqual(20, r['used_np'])
        self.assertEqual(0, r['avail_np'])
        self.assertEqual(6, r['running_jobs'])
        self.assertEqual(1.0, r['np_utilization'])

    def test_does_np_utilization_0(self):
        r = pbsstatus.cluster_info(self.nodes_info)
        self.assertEqual(20, r['total_np'])
        self.assertEqual(0, r['used_np'])
        self.assertEqual(20, r['avail_np'])
        self.assertEqual(0, r['running_jobs'])
        self.assertEqual(0.0, r['np_utilization'])

class TestParseJobString(unittest.TestCase):
    def test_parses_single_cpu(self):
        r = pbsstatus.parse_job_string('0/1.foo')
        self.assertEqual(
            {'ncpus':1,'cpus':[0],'jobid':1,'submit_host':'foo'}, r
        )

    def test_parses_dash_range(self):
        r = pbsstatus.parse_job_string('0-3/1.foo')
        self.assertEqual(
            {'ncpus':4,'cpus':[0,1,2,3],'jobid':1,'submit_host':'foo'}, r
        )

    def test_parses_comma_list(self):
        r = pbsstatus.parse_job_string('0,3,5/1.foo')
        self.assertEqual(
            {'ncpus':3,'cpus':[0,3,5],'jobid':1,'submit_host':'foo'}, r
        )
