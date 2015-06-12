import xml.etree.ElementTree as ET
from . import unittest
from os.path import *

import mock
from nose.plugins.attrib import attr

from pypbs import pbsxml

NODESXML = join(dirname(__file__),'output.xml')
JOBSXML = join(dirname(__file__),'qstat_output.xml')

@attr('current')
class TestParsePbspbsxml(unittest.TestCase):
    def setUp(self):
        tree = ET.parse(NODESXML)
        root = tree.getroot()
        self.nodes = pbsxml.parse_xml(root, 'name')
        tree = ET.parse(JOBSXML)
        root = tree.getroot()
        self.jobs = pbsxml.parse_xml(root, 'Job_Id')

    def test_parses_comma_lists(self):
        self.assertIsInstance(
            self.nodes['host4.example.com']['jobs'], list
        )

    def test_parses_status_jobs(self):
        hostinfo = self.nodes['host3.example.com']
        jobs = hostinfo['status']['jobs']
        self.assertEqual(
            '2600', jobs['656.host1.example.com']['session_id']
        )

    def test_when_only_one_job_still_returns_list(self):
        self.assertEqual(
            ['0,2-4/1.host1.example.com'], self.nodes['host6.example.com']['jobs']
        )

    def test_builds_sub_dict_with_equal_signs(self):
        self.assertEqual(
            '1430334904', self.nodes['host1.example.com']['status']['rectime']
        )
        self.assertEqual(
            None, self.nodes['host1.example.com']['status']['gres']
        )

    def test_parses_job_xml(self):
        self.assertEqual(
            '1.host.example.com',
            self.jobs['1.host.example.com']['Job_Id']
        )
        self.assertEqual(
            '141:00:22',
            self.jobs['1.host.example.com']['resources_used']['cput']
        )

    def test_parses_exec_host_property(self):
        self.assertEqual(
            'host.example.com/0,2-4',
            self.jobs['1.host.example.com']['exec_host']
        )

class TestParseListString(unittest.TestCase):
    def test_returns_original_string(self):
        self.assertEqual('foo', pbsxml.parse_list_string('foo'))

    def test_returns_split_list(self):
        self.assertEqual(
            ['foo','bar'], pbsxml.parse_list_string('foo,bar')
        )

    def test_returns_dictionary(self):
        self.assertEqual(
            {'foo':'bar','baz':None,'bar':'foo'},
            pbsxml.parse_list_string('foo=bar,baz=,bar=foo')
        )

    def test_parses_actual(self):
        status = 'rectime=1430334888,macaddr=00:00:00:00:00:03,cpuclock=OnDemand:2301MHz,varattr=,jobs=656.host1.example.com(cput=704205,energy_used=0,mem=663876kb,vmem=290383028kb,walltime=1143760,session_id=2600) 812.host1.example.com(cput=466890,energy_used=0,mem=851568kb,vmem=286089568kb,walltime=513972,session_id=31317) 851.host1.example.com(cput=171210,energy_used=0,mem=856996kb,vmem=290125588kb,walltime=171501,session_id=17897) 855.host1.example.com(cput=169197,energy_used=0,mem=530380kb,vmem=290383028kb,walltime=169460,session_id=18106) 864.host1.example.com(cput=107891,energy_used=0,mem=941696kb,vmem=290326052kb,walltime=108039,session_id=1350) 865.host1.example.com(cput=107606,energy_used=0,mem=832564kb,vmem=290193180kb,walltime=107777,session_id=1421) 866.host1.example.com(cput=107372,energy_used=0,mem=916400kb,vmem=290324252kb,walltime=107567,session_id=1494) 868.host1.example.com(cput=106830,energy_used=0,mem=830340kb,vmem=290060052kb,walltime=107005,session_id=1830) 870.host1.example.com(cput=106174,energy_used=0,mem=843748kb,vmem=290125588kb,walltime=106340,session_id=2372) 892.host1.example.com(cput=95790,energy_used=0,mem=836868kb,vmem=286180260kb,walltime=95935,session_id=5514) 978.host1.example.com(cput=7449,energy_used=0,mem=846060kb,vmem=290060052kb,walltime=7463,session_id=25749),state=free,netload=622455994750,gres=,loadave=17.77,ncpus=24,physmem=264455068kb,availmem=260210680kb,totmem=272647060kb,idletime=102260,nusers=1,nsessions=11,sessions=25749 5514 2372 1830 1494 1421 1350 18106 17897 31317 2600,uname=Linux host3.example.com 2.6.32-431.20.3.el6.x86_64 #1 SMP Fri Jun 6 18:30:54 EDT 2014 x86_64,opsys=linux'
        r = pbsxml.parse_list_string(status)
        self.assertEqual('1430334888', r['rectime'])
        self.assertIn('656.host1.example.com', r['jobs'])
        self.assertEqual('704205', r['jobs']['656.host1.example.com']['cput'])
        self.assertEqual(11, len(r['jobs']))

class TestParseJobList(unittest.TestCase):
    def test_parses_no_jobs_returns_empty_list(self):
        self.assertEqual([], pbsxml.parse_job_list(''))
    
    def test_parses_single_job(self):
        self.assertEqual(
            ['0,2-4/1.host.example.com'],
            pbsxml.parse_job_list('0,2-4/1.host.example.com')
        )

    def test_parses_multiple_job(self):
        self.assertEqual(
            [
                '0,2-4/1.host.example.com',
                '1,5,7/2.host.example.com'
            ],
            pbsxml.parse_job_list('0,2-4/1.host.example.com,1,5,7/2.host.example.com')
        )
