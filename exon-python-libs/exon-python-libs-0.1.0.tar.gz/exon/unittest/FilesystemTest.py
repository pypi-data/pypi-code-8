__author__ = 'Stephan Conrad <stephan@conrad.pics>'


import unittest
from exon.utils.disk.filesystem import Filesystems, FilesystemException
import shutil
import os


class FilesystemTest(unittest.TestCase):
#class FilesystemTest(object):

    @classmethod
    def setUpClass(cls):
        shutil.copy('/etc/fstab', '/etc/fstab.unit')

    @classmethod
    def tearDownClass(cls):
        shutil.copy('/etc/fstab.unit', '/etc/fstab')
        os.remove('/etc/fstab.unit')


    def test_readFs(self):
        fs = Filesystems()
        mounts = {}
        for mount in fs.fs:
            mounts[mount.mountpoint] = mount
        self.assertIn('/', mounts)
        self.assertTrue(mounts['/'].fstab)
        self.assertIn('/boot', mounts)
        self.assertTrue(mounts['/boot'].fstab)

    def test_addFS(self):
        fs = Filesystems()
        fs.addToFstab('/dev/gibtesnicht', '/unittest/notexists', 'ext4')
        mounts = {}
        fs.refresh()
        for mount in fs.fs:
            mounts[mount.mountpoint] = mount
        self.assertIn('/unittest/notexists', mounts)
        self.assertTrue(mounts['/unittest/notexists'].fstab)
        self.assertRaises(FilesystemException, fs.addToFstab,'/dev/gibtesnicht', '/unittest/notexists')