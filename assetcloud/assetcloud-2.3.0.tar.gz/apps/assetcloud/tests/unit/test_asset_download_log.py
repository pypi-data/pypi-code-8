from django.contrib.auth.models import User
from django.db.models.fields import FieldDoesNotExist, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.test.testcases import TestCase
from django.contrib import admin
from assetcloud.admin import AssetDownloadLogAdmin
from assetcloud.models import AssetDownloadLog, Asset
from assetcloud.tests.contract.utils import TNABotContractTest


class AssetDownloadLogTests(TestCase):

    @TNABotContractTest
    def test_asset_download_log_has_asset_field(self):
        try:
            AssetDownloadLog._meta.get_field("asset")
        except FieldDoesNotExist:
            self.fail("AssetDownloadLog should have an asset field")

    @TNABotContractTest
    def test_asset_field_is_a_foreign_key_to_asset(self):
        asset_field = AssetDownloadLog._meta.get_field("asset")
        self.assertIsInstance(asset_field, ForeignKey)
        self.assertEqual(asset_field.rel.to, Asset)

    @TNABotContractTest
    def test_asset_field_has_correct_related_name(self):
        asset_field = AssetDownloadLog._meta.get_field("asset")
        self.assertEqual("downloads", asset_field.rel.related_name)

    @TNABotContractTest
    def test_asset_download_log_has_user_field(self):
        try:
            AssetDownloadLog._meta.get_field("user")
        except FieldDoesNotExist:
            self.fail("AssetDownloadLog should have a user field")

    @TNABotContractTest
    def test_user_field_is_a_foreign_key_to_user(self):
        user_field = AssetDownloadLog._meta.get_field("user")
        self.assertIsInstance(user_field, ForeignKey)
        self.assertEqual(user_field.rel.to, User)

    @TNABotContractTest
    def test_user_field_has_correct_related_name(self):
        user_field = AssetDownloadLog._meta.get_field("user")
        self.assertEqual("downloads", user_field.rel.related_name)

    def test_user_field_can_be_null(self):
        user_field = AssetDownloadLog._meta.get_field("user")
        self.assertTrue(user_field.blank)
        self.assertTrue(user_field.null)

    def test_asset_download_log_has_datetime_field(self):
        try:
            AssetDownloadLog._meta.get_field("datetime")
        except FieldDoesNotExist:
            self.fail("AssetDownloadLog should have a datetime field")

    def test_datetime_field_is_a_datetime_field(self):
        datetime_field = AssetDownloadLog._meta.get_field("datetime")
        self.assertIsInstance(datetime_field, DateTimeField)

    def test_datetime_field_has_auto_now_add(self):
        datetime_field = AssetDownloadLog._meta.get_field("datetime")
        self.assertTrue(datetime_field.auto_now_add)

    def test_get_display_user_can_get_user_string_if_none(self):
        asset_download_log = AssetDownloadLog()
        asset_download_log.user = None

        self.assertEqual("Public User", asset_download_log.get_user_display())

    def test_download_log_is_registered_in_django_admin_using_admin_class(self):
        self.assertIn(AssetDownloadLog, admin.site._registry)
        self.assertEqual(type(admin.site._registry[AssetDownloadLog]), AssetDownloadLogAdmin)

    def test_download_log_fields_are_read_only_in_admin(self):

        all_fields = [
            "user",
            "datetime",
            "asset"
        ]

        read_only_fields = AssetDownloadLogAdmin.readonly_fields
        self.assertTrue(all(field in read_only_fields for field in all_fields))
