from os import sep, path, makedirs, system
import shutil


class SaddleDir(object):
    def __init__(self, project_directory):
        self.project_directory = project_directory
        self.saddle_dir = project_directory + sep + ".saddle"

    def clean(self):
        if path.exists(self.saddle_dir):
            shutil.rmtree(self.saddle_dir, ignore_errors=True)
        makedirs(self.saddle_dir)
        makedirs(self.stdlogdir())

    def testlog(self):
        return self.saddle_dir + sep + "test.log"

    def stdlogdir(self):
        return self.saddle_dir + sep + "stdlog"

    def faketime(self):
        return self.saddle_dir + sep + "faketime.txt"

    def pgid(self):
        return self.saddle_dir + sep + "saddle.pgid"

    def testcaseout(self):
        return self.stdlogdir() + sep + "testcase.out"

    def testcaseerr(self):
        return self.stdlogdir() + sep + "testcase.err"

    def setup_out(self, name):
        return self.stdlogdir() + sep + name.lower() + "_setup.out"

    def setup_err(self, name):
        return self.stdlogdir() + sep + name.lower() + "_setup.err"

    def poststart(self, name):
        return self.stdlogdir() + sep + name.lower() + "_poststart.out"

    def poststart_err(self, name):
        return self.stdlogdir() + sep + name.lower() + "_poststart.err"
