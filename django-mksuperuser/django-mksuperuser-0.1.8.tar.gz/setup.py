#  -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import django_mksuperuser

setup(
    name='django-mksuperuser',
    version=django_mksuperuser.__version__,
    description='Make super user with fixtures or migrations',
    long_description=open('README.rst').read(),
    author='Michal Klich',
    author_email='michal@michalklich.com',
    include_package_data=True,
    packages=find_packages(),
    url='https://github.com/inirudebwoy/django-mksuperuser',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
