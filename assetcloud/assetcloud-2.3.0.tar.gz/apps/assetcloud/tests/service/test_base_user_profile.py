from django.test.client import RequestFactory
from assetcloud.models import BaseUserProfile
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.utils import TestCase, create_account, create_user
from django.core import mail


class BaseUserProfileTests(TestCase):

    @TNABotContractTest
    def test_can_create_already_active_user_account(self):
        account = create_account()
        user = BaseUserProfile.create_account_user(
            account=account,
            is_active=True
        )

        self.assertTrue(user.is_active)

    @TNABotContractTest
    def test_account_creation_sends_activation_email_if_user_is_not_active(self):
        account = create_account()

        request_factory = RequestFactory()
        request = request_factory.get("/")

        self.assertEqual(len(mail.outbox), 0)
        BaseUserProfile.create_account_user(
            account=account,
            request=request
        )
        self.assertEqual(len(mail.outbox), 1)

    @TNABotContractTest
    def test_account_creation_does_not_send_activation_email_if_created_user_is_active(self):
        account = create_account()

        request_factory = RequestFactory()
        request = request_factory.get("/")

        self.assertEqual(len(mail.outbox), 0)
        BaseUserProfile.create_account_user(
            account=account,
            request=request,
            is_active=True
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_account_creation_does_not_add_activation_key_if_user_is_active(self):
        account = create_account()

        request_factory = RequestFactory()
        request = request_factory.get("/")

        user = BaseUserProfile.create_account_user(
            account=account,
            request=request,
            is_active=True
        )
        self.assertEqual("", user.get_profile().activation_key)

    def get_user_profile_subclass_instance(self):
        class UserProfileSubclass(BaseUserProfile):
            @classmethod
            def get_from_address(cls, *args, **kwargs):
                return 'test@test.com'

            def save(self):
                pass

        return UserProfileSubclass(user=create_user())

    def assertOverriddenEmailUsed(self):
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual('test@test.com', mail.outbox[0].from_email)

    @TNABotContractTest
    def test_get_from_address_can_be_overridden_by_subclass_for_forgotten_password_email(self):
        n = self.get_user_profile_subclass_instance()
        n.send_forgotten_password_email(None)
        self.assertOverriddenEmailUsed()

    @TNABotContractTest
    def test_get_from_address_can_be_overridden_by_subclass_for_delete_user(self):
        n = self.get_user_profile_subclass_instance()
        n.delete_user(None)
        self.assertOverriddenEmailUsed()

    @TNABotContractTest
    def test_get_from_address_can_be_overridden_by_subclass_for_send_activated_email(self):
        n = self.get_user_profile_subclass_instance()
        n.send_activated_email(None)
        self.assertOverriddenEmailUsed()

    @TNABotContractTest
    def test_get_from_address_can_be_overridden_by_subclass_for_send_activation_email(self):
        n = self.get_user_profile_subclass_instance()
        n.send_activation_email(None)
        self.assertOverriddenEmailUsed()
