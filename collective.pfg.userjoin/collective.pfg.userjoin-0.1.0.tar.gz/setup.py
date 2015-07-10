from setuptools import setup, find_packages
import os

version = '0.1.0'

setup(name='collective.pfg.userjoin',
      version=version,
      description="A PloneFormGen adapter for subscribe users to the site",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        ],
      keywords='plone plonegov ploneformgen user subscription',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://github.com/PloneGov-IT/collective.pfg.userjoin',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.pfg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.PloneFormGen',
          'Products.DataGridField>=1.9.0',
          'plone.api',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
