#!/usr/bin/env python 
import os

from distutils.core import setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
        SCRIPT_DIR = os.getcwd()


# put together list of requirements to install
install_requires = []
with open(os.path.join(SCRIPT_DIR, 'requirements.txt')) as fh:
        for line in fh.readlines():
                    if line.startswith('-'):
                                    continue

        install_requires.append(line.strip())


setup(name='discovery',
      version='0.0.4',
      description='Python library for getting values from ETCD',
      author='Roberto Aguilar',
      author_email='roberto@zymbit.com',
      packages=['discovery'],
      long_description=open('README.md').read(),
      url='http://github.com/zymbit/discovery',
      license='LICENSE.txt',
      install_requires=install_requires
)
