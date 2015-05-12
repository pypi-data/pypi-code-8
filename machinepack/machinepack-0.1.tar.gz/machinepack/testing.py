import os
import shutil
import unittest

from click.testing import CliRunner

from machinepack.command_line import cli


class MachineTest(unittest.TestCase):
    def setUp(self):
        self.cli = cli
        self.name = 'test'
        self.package_name = 'machinepack_' + self.name

        shutil.rmtree(self.package_name, ignore_errors=True)

        self.runner = CliRunner()
        result = self.runner.invoke(cli,
                                    ['create', self.name, '--description=Description of machinepack', '--author=test',
                                     '--email=test@test.com'])

        self.assertEqual(result.exit_code, 0)

        os.chdir(self.package_name)

    def tearDown(self):
        os.chdir(os.pardir)
        shutil.rmtree(self.package_name, ignore_errors=True)
