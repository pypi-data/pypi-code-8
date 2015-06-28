__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import unittest
from exon.utils.share.ShareManager import ShareManager
from exon.utils.share.NfsShare import NfsShareService, NfsShare
from exon.utils.share.AfpShare import AfpShareService, AfpShare, AfpAcl
from exon.utils.share.SmbShare import SmbShare, SmbShareService
import os


class ShareTest(unittest.TestCase):
    def setUp(self):
        self.manager = ShareManager()
        os.makedirs('/tmp/unittest')

    def tearDown(self):
        os.removedirs('/tmp/unittest')
        self.manager.delete('unitTest')

    def test_readShare(self):
        shares = self.manager.listShares()
        self.assertIsInstance(shares, dict)
        self.assertIn('sysvol', shares)
        self.assertIn('netlogon', shares)

    def test_MangeSambaShare(self):
        shareData = {
            "unitTest": {
                "smb": {
                    "read_users": [],
                    "valid_groups": [],
                    "write_groups": [],
                    "invalid_users": [],
                    "write_users": [],
                    "invalid_groups": [],
                    "valid_users": [],
                    "read_groups": [],
                },
                "path": "/tmp/unittest"
            }
        }
        self.assertTrue(self.manager.fromJson(shareData))
        share = self.manager.getShare("unitTest")
        self.assertIsInstance(share, dict)
        self.assertEqual(share['smb'].name, 'unitTest')
        self.assertEqual(share['smb'].path, '/tmp/unittest')
        self.assertEqual(share['smb'].options['read only'].lower(), 'no')
        shareData["unitTest"]['smb']["read_users"].append('test')
        self.assertTrue(self.manager.fromJson(shareData))
        share = self.manager.getShare("unitTest")
        self.assertIn('test', share['smb'].acl.read)
        self.assertTrue(self.manager.delete("unitTest"))
        self.manager.listShares()
        self.assertIsNone(self.manager.getShare("unitTest"))

    def test_ManageNfsShare(self):
        shareData = {
            "unitTest": {
                "nfs": {
                    "read_hosts": [
                        "localhost",
                    ],
                    "write_hosts": []
                },
                "path": "/tmp/unittest"
            }
        }
        self.assertTrue(self.manager.fromJson(shareData))
        share = self.manager.getShare("unitTest")
        self.assertIsInstance(share, dict)
        self.assertEqual(share['nfs'].name, 'unitTest')
        self.assertEqual(share['nfs'].path, '/tmp/unittest')
        self.assertIn('localhost', share['nfs'].acl.read)
        shareData["unitTest"]['nfs']["write_hosts"].append('test')
        self.assertTrue(self.manager.fromJson(shareData))
        self.manager.listShares()
        share = self.manager.getShare("unitTest")
        self.assertIn('test', share['nfs'].acl.write)
        self.assertTrue(self.manager.delete("unitTest"))
        self.manager.listShares()
        self.assertIsNone(self.manager.getShare("unitTest"))

    def test_ManageAfpShare(self):
        shareData = {
            "unitTest": {
                "afp": {
                    "valid_groups": [],
                    "invalid_users": [],
                    "valid_users": [
                        "test"
                    ],
                    "invalid_groups": []
                },
                "path": "/tmp/unittest"
            }
        }
        self.assertTrue(self.manager.fromJson(shareData))
        share = self.manager.getShare("unitTest")
        self.assertIsInstance(share, dict)
        self.assertEqual(share['afp'].name, 'unitTest')
        self.assertEqual(share['afp'].path, '/tmp/unittest')
        self.assertIn('test', share['afp'].acl.valid)
        shareData["unitTest"]['afp']["invalid_users"].append('test2')
        self.assertTrue(self.manager.fromJson(shareData))
        self.manager.listShares()
        share = self.manager.getShare("unitTest")
        self.assertIn('test2', share['afp'].acl.invalid)
        self.assertTrue(self.manager.delete("unitTest"))
        self.manager.listShares()
        self.assertIsNone(self.manager.getShare("unitTest"))

    def test_ManageAllShares(self):
        shareData = {
            "unitTest": {
                "nfs": {
                    "read_hosts": [
                        "192.168.1.1"
                    ],
                    "write_hosts": []
                },
                "afp": {
                    "valid_groups": [],
                    "invalid_users": [],
                    "valid_users": [],
                    "invalid_groups": []
                },
                "smb": {
                    "read_users": [
                        ""
                    ],
                    "valid_groups": [],
                    "write_groups": [],
                    "invalid_users": [],
                    "write_users": [],
                    "invalid_groups": [],
                    "valid_users": [],
                    "read_groups": []
                },
                "path": "/tmp/unittest"
            }
        }

        self.assertTrue(self.manager.fromJson(shareData))
        share = self.manager.getShare("unitTest")
        self.assertIsInstance(share, dict)
        self.assertIn('smb', share)
        self.assertIn('nfs', share)
        self.assertIn('afp', share)
        self.assertTrue(self.manager.delete("unitTest"))
        self.manager.listShares()
        self.assertIsNone(self.manager.getShare("unitTest"))
