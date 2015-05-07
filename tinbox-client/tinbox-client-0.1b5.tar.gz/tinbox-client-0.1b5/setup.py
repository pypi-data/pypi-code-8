#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

name = 'tinbox-client'
package_name = name.replace('-', '_')


# Add src dir to path
src_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(src_abs)


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
    with open(os.path.join(src_abs, package_name, 'version.py')) as fp:
        exec(fp.read(), version)

    # Call the module function 'get_version'
    return version['get_version']()


setup(
    name=name,
    version=get_version(),
    author='Joar Wandborg',
    author_email='joar@5monkeys.se',
    package_dir={'': 'src'},  # Our package root is './src/'.
    packages=find_packages(exclude=['_*']),
    install_requires=[
        'requests-oauthlib==0.4.2'
    ]
)
