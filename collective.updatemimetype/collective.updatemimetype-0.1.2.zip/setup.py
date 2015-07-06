# -*- coding: utf-8 -*-
"""Installer for the collective.updatemimetype package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='collective.updatemimetype',
    version='0.1.2',
    description="Plone addon to fix Archetypes file field mimetypes",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Plone',
    author='Godefroid Chapelle',
    author_email='gotcha@bubblenet.be',
    url='http://pypi.python.org/pypi/collective.updatemimetype',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.api',
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
)
