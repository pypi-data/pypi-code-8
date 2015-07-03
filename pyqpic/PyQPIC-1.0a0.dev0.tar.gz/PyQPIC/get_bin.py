import pkg_resources as pkg
import shutil
import os


def get_bin(path=None):
    with pkg.resource_stream('PyQPIC', 'bin/qpic.e') as fid_read:
        if path is None:
            path = os.getcwd()
        with open(path) as fid_write:
            shutil.copyfileobj(fid_read, fid_write)
