# -*- coding: utf-8 -*-
import os.path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def readlines(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).readlines()


setup(
    name='ucloud-cli',
    version=__import__('ucloud_cli.cli').cli.__version__,
    url='https://github.com/likang/ucloud-cli',
    download_url='http://pypi.python.org/pypi/ucloud-cli',
    description='A simple command-line tool for interacting with UCloud API.',
    long_description=read('README.md'),
    license='MIT',
    platforms=['any'],
    packages=['ucloud_cli'],
    author='Kang Li',
    author_email='i@likang.me',
    keywords=['ucloud', 'console', 'commandline', 'command'],
    install_requires=readlines('requirements.txt'),
    entry_points={
        'console_scripts': [
            'ucloud-cli=ucloud_cli:main',
        ],
    },
    package_data={
        '': ['*.json']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
