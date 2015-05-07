# -*- coding: utf-8 -*-
# (c) 2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud import random_utils
from assetcloud.models import  Account
from assetcloud.tests.service.utils import create_account, create_asset, TestCase
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db.utils import DatabaseError
from django.test.utils import override_settings


class StorageQuotaTests(TestCase):
    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=5 * 1024 * 1024 * 1024)
    def test_delete_asset_lowers_storage_for_account(self):
        asset1 = create_asset(content_length=1024)

        asset2 = create_asset(account=asset1.account, content_length=2048)

        account = asset1.account
        account.storage = 3072

        self.assertEqual(3072, account.storage)

        asset1.delete()

        self.assertEqual(2048, account.storage)

        asset2.delete()

        self.assertEqual(0, account.storage)

    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=5 * 1024 * 1024 * 1024)
    def test_save_asset_where_asset_does_not_exist_increases_account_storage(self):
        account = create_account()

        self.assertEqual(0, account.storage)

        create_asset(account=account, content_length=1024)

        self.assertEqual(1024, account.storage)

        create_asset(account=account, content_length=2048)

        self.assertEqual(3072, account.storage)

    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=5 * 1024 * 1024 * 1024)
    def test_save_asset_increasing_file_size_increases_account_storage(self):
        account = create_account()

        self.assertEqual(0, account.storage)

        create_asset(account=account, content_length=1234)

        self.assertEqual(1234, account.storage)

        asset2 = create_asset(account=account, content_length=5678)

        # 1234 + 5678 = 6912
        self.assertEqual(6912, account.storage)

        file = random_utils.random_file_obj(content_length=10000)
        asset2.file = File(file, name='foobar.dat')
        asset2.save()

        # 1234 + 10000 = 11234
        self.assertEqual(11234, account.storage)

    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=5 * 1024 * 1024 * 1024)
    def test_save_asset_decreasing_file_size_decreases_account_storage(self):
        account = create_account()

        self.assertEqual(0, account.storage)

        create_asset(account=account, content_length=1234)

        self.assertEqual(1234, account.storage)

        asset2 = create_asset(account=account, content_length=5678)

        # 1234 + 5678 = 6912
        self.assertEqual(6912, account.storage)

        file = random_utils.random_file_obj(content_length=789)
        asset2.file = File(file, name='foobar.dat')
        asset2.save()

        # 1234 + 789 = 2023
        self.assertEqual(2023, account.storage)

    def test_account_has_storage_limit(self):
        account = create_account()
        # All accounts are trial accounts for the time being
        self.assertEqual(settings.TRIAL_ACCOUNT_STORAGE_LIMIT,
                         account.storage_limit)

    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=1000)
    def test_account_storage_percentage(self):
        account = create_account()
        self.assertEqual(0, account.storage_percentage)

        # Percentage is deliberately not an integer to test that
        # storage_percentage does float division not integer division
        create_asset(account=account, content_length=505)
        self.assertEqual(50.5, account.storage_percentage)

    def test_can_store_large_numbers_of_bytes(self):
        max_value = 2147483650  # Higher than max int value, lower than big int
        account = create_account()
        self.assertEqual(0, account.storage)
        account.storage = max_value
        try:
            account.save()
            self.assertEqual(Account.objects.get(pk=account.pk).storage,
                             max_value)
        except DatabaseError as e:
            self.fail('Should not have errored while saving: %s' % e)


class StorageQuotaValidationTests(TestCase):
    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=1000)
    def test_exceeding_quota_causes_validation_error(self):
        account = create_account()
        create_asset(account=account, content_length=500)

        with self.assertRaises(ValidationError) as cm:
            create_asset(account=account, content_length=501)

        # Uses nbsp now
        # https://code.djangoproject.com/ticket/20246
        self.assertEqual(
            {
                'file': [u'Uploading this 501\xa0bytes file would use too much storage (you are currently using 500\xa0bytes of your 1000\xa0bytes limit)'],
            },
            cm.exception.message_dict)

    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=1000)
    def test_old_size_not_counted_when_updating(self):
        account = create_account()
        asset = create_asset(account=account, content_length=500)

        file = random_utils.random_file_obj(content_length=501)
        asset.file = File(file, name='foobar.dat')
        asset.save()

    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=1000)
    def test_no_storage_reduction_on_asset_file_update_validation_error(self):
        account = create_account()
        asset = create_asset(account=account, content_length=42)

        with self.assertRaises(ValidationError):
            file = random_utils.random_file_obj(content_length=1001)
            asset.file = File(file, name='foobar.dat')
            asset.save()

        account = Account.objects.get(id=account.id)
        self.assertEqual(42, account.storage)
