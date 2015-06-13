import os
import shutil
from tempfile import mkdtemp
import unittest


class BaseSeedTest(unittest.TestCase):

    def setUp(self):
        container_dir = mkdtemp(suffix=self._testMethodName)
        self.pkg_dir = os.path.join(container_dir, 'testpkg')
        os.mkdir(self.pkg_dir)
        os.chdir(self.pkg_dir)

    def tearDown(self):
        shutil.rmtree(self.pk_dir)

    def create_package(self):
        pass
