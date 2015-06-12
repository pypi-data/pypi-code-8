# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='rxjson',
      version='0.3',
      description='JSON RX Schema validation tool',
      long_description=README,
      license='GPLv2.0',
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Intended Audience :: Developers",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
      ],
      author='Ricardo Signes',
      author_email='rjbs@cpan.org',
      maintainer='Rémy Hubscher',
      maintainer_email='hubscher.remy@gmail.com',
      url='https://github.com/spiral-project/rxjson',
      keywords='json schema validation rx rxjson',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
