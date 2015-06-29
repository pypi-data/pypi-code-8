""" EEA Faceted Tool Installer
"""
import os
from setuptools import setup, find_packages

NAME = 'eea.faceted.tool'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="EEA Faceted Tool",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea faceted navigation tool python zope plone',
      author='Alin Voinea',
      author_email='alin@eaudeweb.ro',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea', 'eea.faceted'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'eea.faceted.vocabularies',
          'plone.app.form',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
