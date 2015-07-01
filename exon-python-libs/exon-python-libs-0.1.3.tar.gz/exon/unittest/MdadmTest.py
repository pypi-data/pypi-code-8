__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import unittest

from exonapi.modules.raid import Mdadm, MdDevice, MdadmCreateRaidException, MdadmDeleteRaidException
from exon.utils.command.execute import exec as run
import re
import os, os.path
import simplejson

class DiskSetupException(Exception):
    pass

class MdadmTest(unittest.TestCase):
#class MdadmTest(object):

    disk_size = '1073741824'
    raid = {}

    @classmethod
    def setUpClass(cls):
        cls._disks = []
        for i in range(0,7):
            cls._disks.append(cls._createVirtualDisk(i))

    @classmethod
    def tearDownClass(cls):
        for lo in cls._disks:
            run('losetup -d %s' % lo[1])
            os.unlink(lo[0])

    @classmethod
    def _createVirtualDisk(cls, num):
        filename = '/tmp/exon_api_test-%d.img' % num
        out = run("qemu-img create -f raw {} {}".format(filename, cls.disk_size))
        if out.rc != 0:
            raise DiskSetupException("Cannot create immage")
        ret = run("losetup --show -f -P %s" % filename)
        if ret.rc != 0:
            print('stdout', ret.stdout)
            print('stderr', ret.stderr)
            raise DiskSetupException("Cannot create loopback device")
        return (filename, "".join(ret.stdout).strip())

    def test_ManageRaid5(self):
        mdadm = Mdadm()
        devs = []
        devs.append(os.path.basename(self._disks[0][1]))
        devs.append(os.path.basename(self._disks[1][1]))
        devs.append(os.path.basename(self._disks[2][1]))
        md = mdadm.createRaid(
            name='Raid5',
            level=5,
            part=True,
            devices=devs
        )
        self.raid[5] = md
        self.assertEqual('3', md.numDevices)
        self.assertIn('degraded', md.state)
        s = mdadm.getDevice(uuid=md.uuid)
        self.assertEqual(md.file, s.file)
        size = (int(self.disk_size) * 2) / 1024
        self.assertTrue(
            int(md.size) > (size * 0.95) and
            int(md.size) < (size * 1.05)
        )

        mdadm.delete(device=s)
        mdadm.refresh()
        s2 = mdadm.getDevice(uuid=md.uuid)
        self.assertIsNone(s2)

    def test_ManageRaid1(self):
        mdadm = Mdadm()
        devs = []
        devs.append(os.path.basename(self._disks[3][1]))
        devs.append(os.path.basename(self._disks[4][1]))
        md = mdadm.createRaid(
            name='Raid1',
            level=1,
            part=True,
            devices=devs
        )
        self.raid[1] = md
        self.assertEqual('2', md.numDevices)
        self.assertIn('resyncing', md.state)
        s = mdadm.getDevice(uuid=md.uuid)
        self.assertEqual(md.file, s.file)
        size = (int(self.disk_size)) / 1024
        self.assertTrue(
            int(md.size) > (size * 0.95) and
            int(md.size) < (size * 1.05)
        )

        mdadm.delete(device=s)
        mdadm.refresh()
        s2 = mdadm.getDevice(uuid=md.uuid)
        self.assertIsNone(s2)

    def test_ManageRaid0(self):
        mdadm = Mdadm()
        devs = []
        devs.append(os.path.basename(self._disks[5][1]))
        devs.append(os.path.basename(self._disks[6][1]))
        md = mdadm.createRaid(
            name='Raid0',
            level=0,
            part=True,
            devices=devs
        )
        self.raid[0] = md
        self.assertEqual('2', md.numDevices)
        s = mdadm.getDevice(uuid=md.uuid)
        self.assertEqual(md.file, s.file)
        size = (int(self.disk_size) * 2) / 1024
        self.assertTrue(
            int(md.size) > (size * 0.95) and
            int(md.size) < (size * 1.05)
        )

        mdadm.delete(device=s)
        mdadm.refresh()
        s2 = mdadm.getDevice(uuid=md.uuid)
        self.assertIsNone(s2)