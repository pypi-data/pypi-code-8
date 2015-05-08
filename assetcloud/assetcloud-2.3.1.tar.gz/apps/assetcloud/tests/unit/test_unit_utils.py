from django.test.testcases import TestCase
from assetcloud.random_utils import random_alphanumeric
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud_auth import emailcase
import re


class UnitUtilTests(TestCase):

    @TNABotContractTest
    def test_only_domain_is_being_converted_to_lowercase(self):

        self.assertEqual("ONE@two.com", emailcase("ONE@TWO.COM"))

    @TNABotContractTest
    def test_random_alphanumeric_returns_random_result(self):
        self.assertNotEqual(random_alphanumeric(), random_alphanumeric())

    @TNABotContractTest
    def test_random_alphanumeric_contains_only_alphanumeric(self):
        self.assertIsNotNone(re.match('^[\w]+$', random_alphanumeric()))
