__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import unittest
from exon.utils.systemd.services import Services, Service


class SystemDTest(unittest.TestCase):
#class SystemDTest(object):

    def test_serverviceList(self):
        s = Services()
        serviceList = s.listUnits()
        self.assertIn('dbus.service', serviceList)
        dbus = serviceList['dbus.service']
        self.assertEqual('active', dbus.activeState)

    def test_manageService(self):
        s = Services()
        cron = s.getServiceByName('cronie.service')
        self.assertIsNotNone(cron)
        cron.stop()
        self.assertFalse(cron.running)
        cron.start()
        self.assertTrue(cron.running)