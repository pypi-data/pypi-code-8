#!/usr/bin/env python
from setuptools import setup
import os

# version info
from scout_api import version
__version__ = version.__version__


def read(filename):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as f:
        return f.read()

setup(
    name='scout_api',
    version=str(__version__),
    packages=['scout_api'],
    description='Python Client Library for ScoutApps\'s REST API',
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst') + '\n\n' +
                      read('AUTHORS.rst')),
    url='https://github.com/shortdudey123/python_scout_api/',
    download_url='https://github.com/shortdudey123/python_scout_api/archive/master.tar.gz',
    license='MIT',
    author='Grant Ridder',
    author_email='shortdudey123@gmail.com',
    scripts=['bin/scout-api'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'requests',
    ]
)
