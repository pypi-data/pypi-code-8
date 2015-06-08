import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def trial_temp(request):
    # pytest monkey-patches Failure at some point, and there's an interaction
    # between importing things from Twisted during plugin discovery and
    # pytest-xdist that causes problems capturing error output.
    # Therefore, we import these in here.
    from twisted.python.filepath import FilePath
    from twisted.trial.util import _unusedTestDirectory

    olddir = os.getcwd()
    testdir, testdir_lock = _unusedTestDirectory(FilePath("_trial_temp"))
    os.chdir(testdir.path)

    def teardown_tempdir():
        os.chdir(olddir)
        testdir_lock.unlock()
    request.addfinalizer(teardown_tempdir)
