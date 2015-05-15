from setuptools import setup, find_packages

version = '1.0'

setup(name='wildcard.fixmissing',
      version=version,
      description="a package that allows you to fix missing modules which cause errors with the ZODB",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Nathan Van Gheem',
      author_email='nathan.vangheem@wildcardcorp.com',
      url='https://github.com/collective/wildcard.fixmissing/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['wildcard'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
