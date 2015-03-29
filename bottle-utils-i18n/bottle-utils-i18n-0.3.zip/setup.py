import os
from setuptools import setup, find_packages

import bottle_utils

def read(fname):
    """ Return content of specified file """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSION = bottle_utils.__version__

setup(
    name='bottle-utils-i18n',
    version=VERSION,
    author='Outernet Inc',
    author_email='branko@outernet.is',
    description=('Translation utilities for developing apps with Bottle web '
                 'framework'),
    license='BSD',
    keywords='bottle utils i18n',
    url='http://outernet-project.github.io/bottle-utils/',
    packages=find_packages(),
    long_description=read('README.rst'),
    install_requires=[
        'bottle==0.12.7',
        'bottle-utils-common==%s' % VERSION,
        'bottle-utils-lazy==%s' % VERSION,
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Framework :: Bottle',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
