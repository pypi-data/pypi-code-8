# -*- coding: utf-8 -*-
"""Installer for the collective.navigationtitle package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='collective.navigationtitle',
    version='0.2',
    description="An add-on for Plone that allows to add a title that is used in navigation elements.",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
    ],
    keywords='Python Plone Dexterity',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'https://bluedynamics.com',
    license='GNU General Public Licence',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'plone.behavior',
        'zope.schema',
        'zope.interface',
        'zope.component',

    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
