from django.test.testcases import TestCase
from assetcloud.tests.contract.utils import ContractTest, TNABotContractTest


class ContractUtilTests(TestCase):

    @ContractTest(app="test app")
    def failing_test(self):
        self.fail("With message")

    @TNABotContractTest
    def another_failing_test(self):
        self.fail("With message")

    def test_contract_decorator_decorates_failing_test(self):
        app = "test app"
        try:
            self.failing_test()
        except AssertionError as e:
            self.assertIn(ContractTest.warning % (app, app), e.message)
            self.assertIn("With message", e.message)

    def test_tnabot_contract_decorator_decorates_failing_test(self):
        app = "tnabot"
        try:
            self.another_failing_test()
        except AssertionError as e:
            self.assertIn(ContractTest.warning % (app, app), e.message)
            self.assertIn("With message", e.message)
