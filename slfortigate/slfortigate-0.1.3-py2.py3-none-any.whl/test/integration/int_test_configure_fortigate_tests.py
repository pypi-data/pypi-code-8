#!/usr/bin/env python2
# -*- coding: latin-1 -*-
""" Tests to run against the ConfigureFortigate class. """

__author__ = 'Bruce Potter <bp@us.ibm.com>'
__copyright__ = '2015 IBM'
__license__ = 'EPL-1.0'

import os, unittest

from slfortigate.configure import ConfigureFortigate

class TestBasic(unittest.TestCase):

    def setUp(self):
        if not ('FG_UT_USER' in os.environ and 'FG_UT_PW' in os.environ and 'FG_UT_IP' in os.environ):
            print "You must set FG_UT_USER, FG_UT_PW and FG_UT_IP environment variables to run the integration tests."
            self.assertTrue(False)
        self.user = os.environ['FG_UT_USER']
        self.pw = os.environ['FG_UT_PW']
        self.ip = os.environ['FG_UT_IP']
        self.assertTrue(self.user and self.pw and self.ip)

    def tearDown(self):
        pass

    def test_t1_create(self):
        cf = ConfigureFortigate(self.user, self.pw, self.ip, verbose=False)

        self.assertTrue(True)

    def test_t2_single_get_command(self):
        cf = ConfigureFortigate(self.user, self.pw, self.ip, verbose=True)
        cmds = ['show firewall policy']

        rc, msg = cf.getCommand(cmds)

        self.assertTrue(rc == 0)
        self.assertTrue('show firewall policy' in msg[0])

    def test_t3_multiple_get_command(self):
        cf = ConfigureFortigate(self.user, self.pw, self.ip, verbose=True)
        cmds = ['show firewall policy','show system interface']

        rc, msg = cf.getCommand(cmds)

        self.assertTrue(rc == 0)
        self.assertTrue('show firewall policy' in msg[0])

    def test_t4_multiple_put_command(self):
        cf = ConfigureFortigate(self.user, self.pw, self.ip, verbose=True)
        cmds = ['config firewall policy',
                'edit 20',
                'set srcintf "v1729-inside"',
                'set dstintf "v415-outside"',
                'set srcaddr "all"',
                'set dstaddr "all"',
                'set action accept',
                'set schedule "always"',
                'set service "ANY"',
                'end']

        rc, msg = cf.putConfigCmds(cmds)

        self.assertTrue(rc == 0)

    def test_t5_lockdown(self):
        cf = ConfigureFortigate(self.user, self.pw, self.ip, verbose=True)

        rc, msg = cf.denyAllUserTraffic()

        self.assertTrue(rc == 0)

    def test_t6_nothing_to_delete(self):
        cf = ConfigureFortigate(self.user, self.pw, self.ip, verbose=True)

        rc, msg = cf.denyAllUserTraffic()
        print str(msg)

        self.assertTrue(rc == 1)

    def test_t7_login_error(self):
        self.user = "foobar"
        cf = ConfigureFortigate(self.user, self.pw, self.ip, verbose=True)
        cmds = ['show firewall policy']

        rc, msg = cf.getCommand(cmds)

        self.assertTrue(rc == 2)
        print str(msg)


if __name__ == '__main__':
    unittest.main()

# vim: set ts=4 sw=4 expandtab:
