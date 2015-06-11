# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

requires = [
    'django',
    'pyyaml',
]

develop_requires = [
    'mixer',
]


def long_description():
    curdir = os.path.dirname(__file__)
    readme = os.path.join(curdir, "README.rst")
    with open(readme) as f:
        return f.read()


setup(
    name='django-dbtemplate',
    author='Matvey Kruglov',
    author_email='kubuzzzz@gmail.com',
    url='https://github.com/subuk/django-dbtemplate',
    version='0.4.1',
    description='Allow to override templates from admin interface',
    long_description=long_description(),
    packages=find_packages(exclude=[
        'tests',
        'dbtemplate.tests',
        'dbtemplate.tests.*',
    ]),
    include_package_data=True,
    install_requires=requires,
    extras_require={
        'develop': develop_requires,
    },
    zip_safe=False,
    test_suite='tests.main',
)
