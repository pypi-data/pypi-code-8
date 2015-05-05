import pytest
import shutil
from os.path import splitext, realpath, dirname, join, isfile

from matmodlab import *
from matmodlab.utils.misc import remove
from matmodlab.utils.fileio import filediff

this_directory = dirname(realpath(__file__))
control_file = join(this_directory, 'base.diff')

class StandardTypeTest(object):
    '''Defines setup and teardown methods for standard test'''

    @classmethod
    def setup_class(self):
        self.completed_jobs = []

    @classmethod
    def teardown_class(self):
        '''Removes all test generated files'''
        exts = ('.difflog', '.con', '.log', '.exo', '.dbx', '.eval', '.dat')
        for job in self.completed_jobs:
            for ext in exts:
                remove(join(this_directory, job + ext))

    @staticmethod
    def compare_with_baseline(job, base=None, cf=control_file, interp=0):
        if base is None:
            for ext in ('.base_dbx', '.base_exo', '.base_dat'):
                base = join(this_directory, job.runid + ext)
                if isfile(base):
                    break
            else:
                raise OSError('no base file found for {0}'.format(job.runid))
        f = splitext(job.filename)[0] + '.difflog'
        with open(f, 'w') as fh:
            return filediff(job.filename, base, control_file=cf, stream=fh,
                            interp=interp)
