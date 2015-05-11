# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pinogy_common import __version__

REQUIREMENTS = [
    "django-parler",
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='pinogy-common',
    version=__version__,
    description='Common utilities and code for Pinogy projects.',
    author='Pinogy',
    author_email='info@pinogy.com',
    url='https://bitbucket.org/pinogycorp/pgy-django-common',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
