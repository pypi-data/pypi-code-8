from django.contrib.auth.models import User
from assetcloud.models import Asset
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.utils import TestCase, create_account, create_asset, create_user, get_last_added_user, create_fake_request, create_image_asset


class ServiceUtilTests(TestCase):

    @TNABotContractTest
    def test_create_asset_with_account_creates_asset_with_account(self):
        account = create_account()
        asset = create_asset(account=account)
        retrieved_asset = Asset.unrestricted_objects.get(pk=asset.pk)
        self.assertEqual(retrieved_asset.account, account)
        self.assertEqual(retrieved_asset, asset)

    @TNABotContractTest
    def test_create_image_asset_asset_with_image(self):
        asset = create_image_asset()
        retrieved_asset = Asset.unrestricted_objects.get(pk=asset.pk)
        self.assertTrue(retrieved_asset.file)
        self.assertTrue(retrieved_asset.file.name)
        self.assertEqual(retrieved_asset.file, asset.file)
        self.assertTrue(retrieved_asset.file.name, asset.file.name)

    @TNABotContractTest
    def test_create_user_with_email_parameter_creates_user_with_email(self):
        email = "1@tnabot.com"
        user = create_user(email=email)
        retrieved_user = User.objects.get(pk=user.pk)
        self.assertEqual(retrieved_user.email, email)
        self.assertEqual(retrieved_user, user)

    @TNABotContractTest
    def test_get_last_added_user_gets_last_added_user(self):
        create_user()
        create_user()
        last_added_user = create_user()
        user = get_last_added_user()
        self.assertEqual(user, last_added_user)

    @TNABotContractTest
    def test_create_fake_request_has_get_dictionary(self):
        self.assertEqual({}, create_fake_request().GET)
