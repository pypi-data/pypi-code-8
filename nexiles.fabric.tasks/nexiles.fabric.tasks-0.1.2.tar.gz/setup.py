# -*- coding: utf-8 -*-
"""
This module contains the tool of sample
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.2'

long_description = (
    read('README.rst')
    )

setup(name='nexiles.fabric.tasks',
      version=version,
      description="fabric tasks used at nexiles GmbH",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='',
      author='Stefan Elethofer',
      author_email='stefan.eletzhofer@nexiles.com',
      url='https://skynet.nexiles.com/docs/nexiles.fabric.tasks/',
      license='BSD',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['nexiles', 'nexiles.fabric'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'fabric',
                        # -*- Extra requirements: -*-
                        ],
     entry_points={
          # 'console_scripts': [
          #     'nxtools = nexiles.fabric.tasks.main:main',
          #     ]
          }
      )
