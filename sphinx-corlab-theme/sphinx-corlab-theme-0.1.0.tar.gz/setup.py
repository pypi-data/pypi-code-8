"""
Setup script for the CoR-Lab sphinx theme.

.. codeauthor:: Johannes Wienke <jwienke@techfak.uni-bielefeld.de>
"""

import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string."""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='sphinx-corlab-theme',
    version=__import__('corlab_theme').__version_full__,
    author='Johannes Wienke',
    author_email='jwienke@techfak.uni-bielefeld.de',
    packages=find_packages(),
    include_package_data=True,
    url='https://code.cor-lab.org/projects/sphinx-corlab-theme',
    license='LGPLv3+',
    description=u' '.join(
        __import__('corlab_theme').__doc__.splitlines()).strip(),
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation'
    ],
    install_requires=('sphinx>=1.2'),
    long_description=read_file('README.rst'),
    zip_safe=False,
)
