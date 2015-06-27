""" goulash._os
"""
import os, errno
import time, stat
from goulash.python import get_env

# copy-tree with overwrites (unlike shutil.copytree)
from distutils.dir_util import copy_tree  # NOQA
from distutils.file_util import copy_file  # NOQA

def home():
    return get_env('HOME')
get_home = home

def touch(fname, times=None):
    """ similar to shell command 'touch' """
    with open(fname, 'a'):
        os.utime(fname, times)
touch_file = touch

def file_age_in_seconds(pathname):
    if not os.path.exists(pathname):
        return None
    return time.time() - os.stat(pathname)[stat.ST_MTIME]

# SOURCE:
#  http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
    """ os.makedirs() is a constant annoyance since it is
        close to having this functionality, but always dies
        if the argument already exists
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
makedirs = mkdirs = mkdir_p

def which(name):
    return os.popen('which ' + name).readlines()[0].strip()

def get_mounts_by_type(mtype):
    tmp = os.popen('mount -l -t {0}'.format(mtype))
    tmp = tmp.readlines()
    tmp = [x.strip() for x in tmp if x.strip()]
    tmp2 = []
    for line in tmp:
        mdata = dict(line=line)
        line = line.split(' on ')
        name = line.pop(0)
        line = ''.join(line)
        line = line.split(' type ')
        mount_point = line.pop(0)
        mdata.update(name=name, mount_point=mount_point)
        tmp2.append(mdata)
    return tmp2

def summarize_fpath(fpath):
    """ truncates a filepath to be more suitable for display.
        every instance of $HOME is replaced with ~
    """
    if home():
        return fpath.replace(home(), '~')
