# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

MODULE = 'djcron_agent'


def read_file(filename):
    with open(filename) as fd:
        return fd.read()


def app_info():
    version_file = os.path.join(MODULE, 'versions.py')
    local = dict()
    exec(read_file(version_file), local)
    return local.get('APP')


APP = app_info()


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args or ['--cov-report=term-missing'])
        sys.exit(errno)


setup(
    name=MODULE.replace('_', '-'),
    version=APP.version,
    description=APP.description,
    long_description=read_file('README.rst'),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    keywords='distributed cron',
    author='Miguel Ángel García',
    author_email='miguelangel.garcia@gmail.com',
    url='https://github.com/djcron-project/djcron-agent',
    license='Affero',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    install_requires=[
        'celery >= 3.1.12',
        'psutil >= 2.1.3',
    ],
    extras_require={
        'redis': ['redis  >= 2.10.3'],
    },
)
