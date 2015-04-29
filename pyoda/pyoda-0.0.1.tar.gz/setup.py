#!/usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

import pyoda

setup(
    name = 'pyoda',
    version = pyoda.VERSION,
    author = 'Adria Casajus<acasajus@cloudjutsu.com>',
    author_email = 'acasajus@cloudjutsu.com',
    license = "MIT",
    url = "https://bitbucket.org/cloudjutsu/pyoda",
    packages = [ 'pyoda' ],
    description='Python library for ODA',
    long_description=open( 'README.txt' ).read(),
    install_requires=[
      "pyyaml > 3.0",
      "python-keyczar >= 0.715",
      "pbkdf2 >= 1.3"
      ],
    entry_points = { 'console_scripts': [
      'oda_register_host = pyoda.scripts.registerhost:run',
      'oda_get_hosts = pyoda.scripts.gethosts:run',
      'oda_view_host_ciphered_data = pyoda.scripts.viewhostcredentials:run'
      ],
      },

    )
