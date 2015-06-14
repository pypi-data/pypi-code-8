#  -*- coding: utf-8 -*-
import django_freezer

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='django-freezer',
    version=django_freezer.__version__,
    description='Print pip freeze in your admin panel',
    long_description=open('README.rst').read(),
    author='Michal Klich',
    author_email='michal@michalklich.com',
    include_package_data=True,
    packages=['django_freezer'],
    url='https://github.com/inirudebwoy/django-freezer',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
