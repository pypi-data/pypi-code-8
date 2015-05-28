from setuptools import setup, Extension

import os



setup(name='PyInABox',
      version='1.0.1',
      description='Implementation of shell running on top of python-vte and Athena LivePage',
      author='Logan Perkins',
      author_email='perkins@injeanieousdesigns.com',
      url='https://github.com/perkinslr/PyInABox',
      packages=['PyInABox'],
      requires = ['zope.interface', 'nevow'],
      license = "ZLIB",
      keywords = "vte COMET AJAX",
      long_description=open('README.md').read(),

     )


