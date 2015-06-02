# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2.2'

long_description = (read('README.rst') + '\n' + read('CONTRIBUTORS.rst'))
entry_point = 'buildout.requirements:install'
entry_points = {'zc.buildout.extension': ['ext = %s' % entry_point]}

tests_require = ['zc.buildout', 'zope.testing', 'zc.recipe.egg']

setup(name='buildout.requirements',
      version=version,
      description='Dump buildout picked versions '
      'as a pip compatible requirements.txt file. Fork of buildout.dumprequirements.',
      long_description=long_description,
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      license='GPL',
      keywords='buildout extension dump picked versions requirements.txt',
      author='Yves Müller',
      author_email='yves.mueller@liqd.de',
      url='https://github.com/liqd/buildout.requirements',
      packages=find_packages(),
      namespace_packages=['buildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points=entry_points)
