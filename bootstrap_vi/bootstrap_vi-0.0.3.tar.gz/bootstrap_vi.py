from __future__ import print_function

import subprocess
import sys
import re
from os.path import join, basename, abspath

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    from __builtin__ import open
except ImportError:
    from builtins import open

PYPI_DL_URL = 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-{VER}.tar.gz'
PYPI_VI_URL = 'https://pypi.python.org/pypi/virtualenv'

try:
    from setuptools import Command
except ImportError:
    Command = BootstrapVI = None
else:
    class BootstrapVI(Command):
        description = 'Bootstrap virtualenv(All virtualenv arguments supported)'
        user_options = []
        command_consumes_arguments = True

        def initialize_options(self):
            self.args = []

        def finalize_options(self):
            pass

        def run(self):
            bootstrap_vi(venvargs=self.args)

class VersionError(Exception):
    '''
    Generic error fetching version
    '''
    pass

def get_venv_args(argv):
    '''
    Get only the args for virtualenv
    '''
    if not argv:
        return []
    if argv[0] == '-':
        return argv[1:]
    elif 'bootstrap_vi' in argv[0]:
        return argv[1:]
    return argv

def get_latest_virtualenv_version():
    '''
    Fetch pypi page for virtualenv and parse out latest version

    :return str: version string(Ex. 13.1.0)
    '''
    data = urlopen(PYPI_VI_URL).read()
    if isinstance(data, bytes):
        html = data.decode('utf-8')
    else:
        html = data
    m = re.search('virtualenv (\d+\.\d+\.\d+)', html)
    if not m:
        raise VersionError("Cannot get latest version from PYPI")
    return m.group(1)

def download_virtualenv(version, dldir=None):
    '''
    Download virtualenv package from pypi and return response that can be
    read and written to file

    :param str version: version to download or latest version if None
    :param str dldir: directory to download into or None for cwd
    '''
    dl_url = PYPI_DL_URL.format(VER=version)
    filename = basename(dl_url)
    if dldir:
        dl_path = join(dldir, filename)
    else:
        dl_path = filename
    data = urlopen(PYPI_DL_URL.format(VER=version))
    with open(dl_path, 'wb') as fh:
        fh.write(data.read())
    return dl_path

def create_virtualenv(venvpath, venvargs=None):
    '''
    Run virtualenv from downloaded venvpath using venvargs
    If venvargs is None, then 'venv' will be used as the virtualenv directory

    :param str venvpath: Path to root downloaded virtualenv package(must contain
        virtualenv.py)
    :param list venvargs: Virtualenv arguments to pass to virtualenv.py
    '''
    cmd = [join(venvpath, 'virtualenv.py')]
    venv_path = None
    if venvargs:
        cmd += venvargs
        venv_path = abspath(venvargs[-1])
    else:
        cmd += ['venv']
    p = subprocess.Popen(cmd)
    p.communicate()

def bootstrap_vi(version=None, venvargs=None):
    '''
    Bootstrap virtualenv into current directory

    :param str version: Virtualenv version like 13.1.0 or None for latest version
    :param list venvargs: argv list for virtualenv.py or None for default
    '''
    if not version:
        version = get_latest_virtualenv_version()
    tarball = download_virtualenv(version)
    p = subprocess.Popen('tar xzvf {0}'.format(tarball), shell=True)
    p.wait()
    p = 'virtualenv-{0}'.format(version)
    create_virtualenv(p, venvargs)

def main():
    venv_args = get_venv_args(sys.argv)
    bootstrap_vi(venvargs=venv_args)

if __name__ == '__main__':
    main()
