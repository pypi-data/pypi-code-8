#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

from setuptools import setup

VERSION_FILE = "source/sniprd/_version.py"
VERSION_EXEC = ''.join(open(VERSION_FILE).readlines())
__version__ = ''
exec(VERSION_EXEC)  # update __version__
if not __version__:
    raise RuntimeError("Unable to find version string in %s." % VERSION_FILE)

# Parse the version and release from master spec file
# RPM spec file is in the parent directory
# import re
# spec_pth = 'sniprd.spec'
# with open(spec_pth) as f:
#    lines = "\n".join(l.rstrip() for l in f)
#    version = re.search('Version: (.+)', lines).group(1).rstrip()
#    release = re.search('Release: (\d+)', lines).group(1).rstrip()
# __version__ = '.'.join([version, release])
# __version__ = '.'.join([version, release])

# acceptable version schema: major.minor[.patch][sub]
__pkg__ = 'sniprd'
__pkgdir__ = {'sniprd': 'source/sniprd'}
__pkgs__ = [
    'sniprd',
]
__provides__ = ['sniprd']
__desc__ = 'Status Report - Comfortable CLI Activity Status Reporting'
__scripts__ = ['source/snip']
__irequires__ = [
    'python_dateutil==2.4.2',
    'sqlalchemy==1.0.0',
]
pip_src = 'https://pypi.python.org/packages/source'
__deplinks__ = []

# README is in the parent directory
readme_pth = 'README.rst'
with open(readme_pth) as _file:
    readme = _file.read()

github = 'https://github.com/kejably2/sniprd'
download_url = '%s/archive/master.zip' % github

default_setup = dict(
    url=github,
    license='GPLv2',
    author='Chris Ward',
    author_email='cward@redhat.com',
    maintainer='Chris Ward',
    maintainer_email='cward@redhat.com',
    download_url=download_url,
    long_description=readme,
    data_files=[],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        'Topic :: Utilities',
    ],
    keywords=['information', 'postgresql', 'tasks', 'snippets'],
    dependency_links=__deplinks__,
    description=__desc__,
    install_requires=__irequires__,
    name=__pkg__,
    package_dir=__pkgdir__,
    packages=__pkgs__,
    provides=__provides__,
    scripts=__scripts__,
    version=__version__,
    zip_safe=False,  # we reference __file__; see [1]
)

setup(**default_setup)
