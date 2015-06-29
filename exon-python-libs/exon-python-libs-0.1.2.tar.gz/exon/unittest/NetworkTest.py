__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import unittest
from exon.utils.arch.netctl import Netctl, NetctlInterface, NetFieldErrorException, Netdev, getAllNics
import os


class NetworkTests(unittest.TestCase):
#class NetworkTests(object):

    def test_getAllNics(self):
        nics = []

        for nic in os.listdir('/sys/class/net/'):
            if nic != 'lo':
                nics.append(nic)

        enic = getAllNics()

        self.assertEqual(len(nics), len(enic))

        for n in enic:
            self.assertIn(n, nics, '%s not found in /sys/class/net/' % n)

    def test_NicDetails(self):
        net = Netctl()
        nics = net.getAllInterfaces()
        self.assertIn('eth0', nics)
        nic = net.getInterface('eth0')
        self.assertGreaterEqual(len(nic.ipaddress), 1)
        self.assertGreaterEqual(len(nic.current_dns), 1)
        self.assertNotEqual("", nic.ip)

    def test_NicCreate(self):
        nic = NetctlInterface(name='unittest1')
        nic.ip = 'dhcp'
        nic.interface = 'unittest1'
        nic.connection = 'ethernet'
        nic.description = 'Interface unittest1'
        nic.write()
        netctl = Netctl()
        self.assertIn('unittest1', netctl.getAllInterfaces())
        netctl.deleteIf('unittest1')
        netctl = Netctl()
        self.assertNotIn('unittest1', netctl.getAllInterfaces())

    def test_NicFromJson(self):
        map = {
                "config": {
                    "gateway": "''",
                    "interface": "unittest1",
                    "routes6": [],
                    "dns": [],
                    "ip": "dhcp",
                    "address6": [],
                    "address": [],
                    "description": "'Interface unittest1'",
                    "ip6": "stateless",
                    "connection": "ethernet",
                    "routes": [],
                    "gateway6": ""
                },
                "name": "unittest1",
                "current": {
                    "status": "down",
                    "ip": [],
                    "ip6": [],
                    "mac": "",
                    "dns": [],
                    "routes": {}
                },
                "enabled": False
            }
        nic = NetctlInterface.fromApiJson(map)
        self.assertEqual('unittest1', nic.interface)
        nic.write()
        netctl = Netctl()
        self.assertIn('unittest1', netctl.getAllInterfaces())
        netctl.deleteIf('unittest1')
        netctl = Netctl()
        self.assertNotIn('unittest1', netctl.getAllInterfaces())

        map2 = {
                "config": {
                    "gateway": "''",
                    "interface": "unittest1",
                    "routes6": [],
                    "dns": [],
                    "ip": "dhcp",
                    "address6": [],
                    "address": [],
                    "description": "'Interface unittest1'",
                    "ip6": "",
                    "connection": "ethernet",
                    "routes": [],
                    "gateway6": ""
                },
                "name": "unittest1",
                "current": {
                    "status": "down",
                    "ip": [],
                    "ip6": [],
                    "mac": "",
                    "dns": [],
                    "routes": {}
                },
                "enabled": False
            }
        self.assertRaises(NetFieldErrorException, NetctlInterface.fromApiJson, map2)
