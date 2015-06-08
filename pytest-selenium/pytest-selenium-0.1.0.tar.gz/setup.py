#!/usr/bin/env python
from setuptools import Command, setup


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='pytest-selenium',
    version='0.1.0',
    description='A selenium plugin for pytest',
    author='codingjoe',
    url='https://github.com/codingjoe/pytest-selenium',
    author_email='info@johanneshoppe.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['pytest_selenium'],
    include_package_data=True,
    install_requires=[
        'pytest>=2.5',
        'selenium',
    ],
    cmdclass={'test': PyTest},
    entry_points={'pytest11': ['django = pytest_selenium.plugin']},
)
