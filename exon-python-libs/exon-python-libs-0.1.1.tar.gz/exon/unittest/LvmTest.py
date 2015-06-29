__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import unittest
import os
from exon.utils.command.execute import exec as run
from exon.utils.disk.lvm import LVM, LVMVolumeGroupError, LVMLogicalVolumeError
from time import sleep

class DiskSetupException(Exception):pass

class LvmTest(unittest.TestCase):
#class LvmTest(object):
    disk_size = '1073741824'
    raid = {}


    def setUp(self):
        self._disks = self._createVirtualDisk(1)


    def tearDown(self):
        run('losetup -d %s' % self._disks[1])
        os.unlink(self._disks[0])


    def _createVirtualDisk(self, num):
        filename = '/tmp/exon_api_test-%d.img' % num
        out = run("qemu-img create -f raw {} {}".format(filename, self.disk_size))
        if out.rc != 0:
            raise DiskSetupException("Cannot create immage")
        ret = run("losetup --show -f -P %s" % filename)
        if ret.rc != 0:
            print('stdout', ret.stdout)
            print('stderr', ret.stderr)
            raise DiskSetupException("Cannot create loopback device")
        return (filename, "".join(ret.stdout).strip())


    def test_VG(self):
        lvm = LVM()
        vg = lvm.createVolumeGroup(name='UnitTestVG', device=self._disks[1])
        self.assertEqual(vg['name'], 'UnitTestVG')
        self.assertEqual(vg['pv'], self._disks[1])
        self.assertIn('UnitTestVG', lvm.getVolumeGroup())
        self.assertTrue(lvm.deleteVolumeGroup(vg['name']))
        lvm.refresh()
        lvm.getVolumeGroup()
        self.assertNotIn('UnitTestVG', lvm.getVolumeGroup())


    def test_LV(self):
        lvm = LVM()
        vg = lvm.createVolumeGroup(name='UnitTestVG', device=self._disks[1])
        lv = lvm.createLogicalVolume('lv1', 'UnitTestVG', size=(20 * 1024 * 1024))
        self.assertEqual('20971520', lv['size'])
        lv2 = lvm.createLogicalVolume('lv1', 'UnitTestVG', size=(40 * 1024 * 1024))
        self.assertEqual('41943040', lv2['size'])

        self.assertRaises(LVMLogicalVolumeError, lvm.createLogicalVolume, 'lv1', 'UnitTestVG', 512)

        self.assertRaises(LVMVolumeGroupError,lvm.deleteVolumeGroup, 'UnitTestVG')
        self.assertTrue(lvm.deleteLogicalVolume(lv['name'], vg['name']))
        lvm.refresh()
        self.assertTrue(lvm.deleteVolumeGroup(vg['name']))
        lvm.refresh()
        self.assertNotIn('UnitTestVG', lvm.getVolumeGroup())