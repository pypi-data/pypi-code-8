import os
import subprocess
import inspect
import pyuv


class Runner(object):
    """Test runner."""
    def __init__(self, pythonpath, filename, repeat=1):
        self.pythonpath = pythonpath
        self.filename = filename
        self.module_name = filename.replace(".py", "").replace(os.sep, ".")

    def runonce(self):
        """Runs a test once and returns true if passed, false if failed."""
        return subprocess.call([self.pythonpath, "-m", self.module_name]) == 0

    def multiple(self, repeat):
        """Runs a test multiple times and returns the percentage pass rate."""
        passes = 0
        for _ in xrange(0, repeat):
            if self.runonce(): passes = passes + 1

        return 100 * float(passes) / float(repeat)