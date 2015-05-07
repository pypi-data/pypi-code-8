#!/usr/bin/env python
from os import path
import sys

from setuptools import setup, find_packages

from pkg_resources import resource_filename

name = 'tinbox-client'
package_name = name.replace('-', '_')

here = path.dirname(path.abspath(__file__))

# Add src dir to path
src_abs = path.join(here, 'src')
sys.path.append(src_abs)


# Get the long description from the relevant file
long_description = None

try:
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    pass


def get_version():
    """
    Get the version from a version module inside our package. This is
    necessary since we import our main modules in package/__init__.py,
    which will cause ImportErrors if we try to import package/version.py
    using the regular import mechanism.

    :return: Formatted version string
    """
    version = {}

    # exec the version module
    with open(resource_filename(package_name, 'version.py')) as fp:
        exec(fp.read(), version)

    # Call the module function 'get_version'
    return version['get_version']()


setup(
    name=name,
    version=get_version(),
    author='Joar Wandborg',
    author_email='joar@5monkeys.se',
    description='Tinbox client library',
    long_description=long_description,
    package_dir={'': 'src'},  # Our package root is './src/'.
    packages=find_packages(exclude=['_*']),
    install_requires=[
        'requests-oauthlib==0.4.2'
    ]
)
