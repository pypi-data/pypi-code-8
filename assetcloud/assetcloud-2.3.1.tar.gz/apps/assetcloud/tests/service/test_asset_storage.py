# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.tests.service.utils import create_asset, TestCase
from django.core.files.base import ContentFile
import random
from assetcloud.models import Asset, get_asset_storage
from assetcloud.tests.service import utils
from assetcloud.upload_history import upload_asset


class AssetStorageFilenameClashTests(TestCase):
    def test_assets_with_same_filename_can_have_different_contents(self):
        """
        This test has always passed when ASSET_FILE_STORAGE =
        'django.core.files.storage.FileSystemStorage'. We wrote this test to
        illustrate a user-visible problem when ASSET_FILE_STORAGE =
        'storages.backends.s3boto.S3BotoStorage': if you upload two assets
        with different files with the same filename then the second file will
        overwrite the first.

        Note: this test will fail if you set ASSET_FILE_STORAGE =
        'storages.backends.s3boto.S3BotoStorage'. Instead, set
        ASSET_FILE_STORAGE = 'assetcloud.storage.S3BotoStorage' (this is a
        subclass with a fix for the overwrite problem).
        """
        # Create two assets with the same name but different (random) contents
        asset1 = create_asset(filename='same.jpg')
        asset2 = create_asset(filename='same.jpg')

        # files should be different
        self.assertNotEqual(asset1.id, asset2.id)
        with self.open_underlying_file(asset1) as file1:
            with self.open_underlying_file(asset2) as file2:
                self.assertNotEqual(file1.read(), file2.read(),
                                    msg='Files read from asset storage should '
                                    'be different, but they were the same')

        # but user-visible filenames should be the same
        self.assertEqual(asset1.filename, asset2.filename)

        # and storage filenames should be based on the user-visible filename
        # (this is not a hard and fast requirement, but it makes it easier
        # to find files manually or recover files if the database becomes
        # corrupt)
        self.assertTrue(asset1.file.name.endswith('.jpg'))
        self.assertTrue(asset1.file.name.startswith('assets/same'))

    def open_underlying_file(self, asset):
        """
        Open an asset's file in the underlying (i.e. back end) storage, not
        a local cache
        """
        return asset.file.storage._open(asset.file.name)


class AssetStorageTests(TestCase):
    def setUp(self):
        super(AssetStorageTests, self).setUp()
        self.file_name = 'test_%s.txt' % str(random.random())
        self.file_contents = 'examplecontents'

        # In-memory file object.
        self.file = ContentFile(self.file_contents)
        self.file.name = self.file_name

        self.user = utils.create_user()
        self.account = self.user.get_profile().account

    def test_save_asset(self):
        asset = Asset(file=self.file, account=self.account)
        upload_asset(asset, added_by=self.user)

        # Ensure that the file is in S3
        self.assertTrue(get_asset_storage().exists(asset.file.name))
        get_asset_storage().delete(asset.file.name)

    def test_delete_asset(self):
        asset = Asset(file=self.file, account=self.account)
        upload_asset(asset, added_by=self.user)

        # Ensure that the file is in storage
        self.assertTrue(get_asset_storage().exists(asset.file.name))

        asset.delete()

        # Ensure that the file is no longer in storage
        self.assertFalse(get_asset_storage().exists(asset.file.name))
