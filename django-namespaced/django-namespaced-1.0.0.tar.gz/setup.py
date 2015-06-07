#!/usr/bin/env python

import os
from setuptools import setup

import versioneer
from pip.download import PipSession
from pip.req import parse_requirements


def get_requirements(filename):
    ''' Parse a pip-style requirements.txt file to setuptools format '''
    install_reqs = parse_requirements(filename, session=PipSession())
    return [str(ir.req) for ir in install_reqs]


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(name='django-namespaced',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Automagic url namespace resolution',
      long_description=README,
      author='Ferrix Hovi',
      author_email='ferrix@codetry.fi',
      install_requires=get_requirements('requirements.txt'),
      setup_requires=get_requirements('development.txt'),
      packages=['namespaced'],
      url='https://github.com/codetry/django_namespaced/',
      license='MIT License',
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 1.8',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      )
