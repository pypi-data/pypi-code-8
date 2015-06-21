#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = ['nucleo.migrations', 'nucleo.fixtures']
version = __import__('nucleo').__version__


def get_required():
    required_txt = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    return open(required_txt).readlines()

extras = {
    'develop': [
        'nose',
    ]
}

setup(
    name='nucleo',
    version=version,
    url='https://github.com/Naible/django-nucleo/',
    author='Naible',
    author_email='admin@naible.com',
    description=('A django app for building social networks.'),
    license='GPLv3+',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    install_requires=get_required(),
    extras_require=extras,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

