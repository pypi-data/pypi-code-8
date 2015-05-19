#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'Django>=1.5.1',
    'six>=1.9.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='django_molder',
    version='0.1.0',
    description="Another one painless way to working with forms and they fields",
    long_description=readme + '\n\n' + history,
    author="Vladimir Savin",
    author_email='zero13cool@yandex.ru',
    url='https://github.com/zerc/django_molder',
    packages=[
        'django_molder',
        'django_molder/renderers',
        'django_molder/templatetags'
    ],
    package_data={
        'django_molder': [
            'templates/django_molder/*',
        ],
    },
    package_dir={'django_molder':
                 'django_molder'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='django_molder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
