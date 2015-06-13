from seed.commands.create import CreateCommand
from tests import BaseSeedTest


class TestCreateCommand(BaseSeedTest):

    def setUp(self):
        super(TestCreateCommand, self).setUp()
        self.cmd = CreateCommand()

    def test_simple(self):
        self.cmd.run()
