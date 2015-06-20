#!/usr/bin/env python

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.default_args = ['-v', '--cov', 'sunset', '--no-cov-on-fail']
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        args = list(self.default_args)

        if isinstance(self.pytest_args, basestring):
            args.append(self.pytest_args)
        else:
            args.extend(self.pytest_args)

        errno = pytest.main(args)
        sys.exit(errno)


setup(
    name='sunset',
    version='0.1.1',
    packages=['sunset'],
    author='Jimmy Shen',
    author_email='thejimmyshen@gmail.com',
    description=(
        'Have you ever added a hack that you told yourself '
        'you would remember to get rid of later on but it eventually '
        'becomes a permanent fixture of the codebase? '
        'With Sunset, simply annotate your code with special comments '
        'and the scanner will alert you when time has come to clean '
        'up your code!'),
    license='MIT',
    entry_points={'console_scripts': ['sunset = sunset.bin:main']},
    install_requires=['pytest', 'pytest-cov', 'mock'],
    url='https://github.com/jimmyshen/sunset',
    download_url='https://github.com/jimmyshen/sunset/tarball/0.1.1',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License'
    ],
    cmdclass={'test': PyTest}
)
