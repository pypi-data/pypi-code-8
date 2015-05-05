#!/usr/bin/env python

import os,sys, shlex, subprocess
from os.path import join
import platform
import distutils
from distutils import sysconfig
from setuptools import find_packages
from distutils.core import setup


__version__ = ''
with open('lib/orphHCA/__init__.py') as inp:
  for line in inp:
      if line.startswith('__version__'):
          exec(line.strip())
          break
          
PACKAGES = ['orphHCA']

PACKAGE_DIR = {}
for pkg in PACKAGES:
    PACKAGE_DIR[pkg] = join('lib', *pkg.split('.'))

SCRIPTS = ['scripts/orphHCA','scripts/filterOrphHCA',]

if (platform.system() == 'Windows' or 
    len(sys.argv) > 1 and sys.argv[1] not in ('build', 'install')):
    for script in list(SCRIPTS):
        SCRIPTS.append(script + '.bat')

setup(
    name='orphHCA',
    version=__version__,
    author='Tristan Bitard-Feildel',
    author_email='t.bitard.feildel@uni-muenster.de',
    url='http://www.bornberglab.org/',
    description='Combined Pfam and HCA ananlysis to improve domain annotation',
    long_description="",
    license='GPL',
    keywords=('protein, domain, HCA, evolution, '),
    classifiers=[
                 'Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Science/Research',
                 'Operating System :: MacOS',
                 'Operating System :: POSIX',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Topic :: Scientific/Engineering :: Bio-Informatics',
                ],
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    scripts=SCRIPTS,
    provides=['orphHCA ({0:s})'.format(__version__)],
)




