import os

import pytest
from twisted.python.filepath import FilePath
from twisted.trial.util import _unusedTestDirectory


@pytest.fixture(scope="session", autouse=True)
def trial_temp(request):
    olddir = os.getcwd()
    testdir, testdir_lock = _unusedTestDirectory(FilePath("_trial_temp"))
    os.chdir(testdir.path)

    def teardown_tempdir():
        os.chdir(olddir)
        testdir_lock.unlock()
    request.addfinalizer(teardown_tempdir)
