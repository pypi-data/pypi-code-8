# -*- coding: utf-8 -*-
from setuptools import setup
import meta

setup(
    name='ud-django-meta',
    description='Pluggable app for handling webpage meta tags and OpenGraph '
    'properties',
    long_description=open('README.rst').read(),
    version=meta.__version__,
    packages=['meta', 'meta.templatetags'],
    package_data={
        'meta': ['templates/*.html'],
    },
    maintainer='Udemy Developers',
    maintainer_email='dev@udemy.com',
    url='https://github.com/udemy/django-meta',
    license='BSD',
    install_requires=[
        'Django>=1.4',
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)


