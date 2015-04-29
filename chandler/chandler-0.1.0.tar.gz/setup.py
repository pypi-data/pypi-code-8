# -*- coding: utf-8 -*-
import re
import os.path as op
from setuptools import setup


def read(filename):
    ''' Return the file content. '''
    with open(op.join(op.abspath(op.dirname(__file__)), filename)) as fd:
        return fd.read()


def get_version():
    return re.compile(r".*__version__ = '(.*?)'", re.S)\
             .match(read(op.join('chandler', '__init__.py'))).group(1)


setup(
    name='chandler',
    author='Bruno Bzeznik',
    author_email='Bruno.Bzeznik@imag.fr',
    version=get_version(),
    url='https://github.com/oar-team/chandler',
    install_requires=[
        'requests',
        'natsort',
        'colorama',
    ],
    packages=['chandler'],
    package_data={
        'chandler': ['*.conf'],
    },
    zip_safe=False,
    description='A simple CLI utility displaying OAR cluster information '
                'retrieved from the API.',
    license="GNU GPL v2",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',  # noqa
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
    ],
    entry_points='''
        [console_scripts]
        chandler=chandler.main:main
    ''',
)
