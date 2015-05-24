#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-third-party',
    version='0.1.0',
    description='Add third party scripts and css to specific paths via db.',
    author='Buddy Lindsey',
    author_email='buddy@buddylindsey.com',
    url='https://github.com/buddylindsey/django-third-party',
    packages=[
        'djthirdparty', 'djthirdparty.migrations'],
    install_requires=[
        'Django>=1.8', 'six', 'django_extensions'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Site Management'],
)
