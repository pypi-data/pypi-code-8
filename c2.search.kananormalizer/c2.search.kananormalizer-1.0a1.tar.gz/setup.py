from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='c2.search.kananormalizer',
      version=version,
      description="This package is Japanese KANA normalizer for Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone search Japanese normalizer',
      author='Manabu TERADA',
      author_email='terada@cmscom.jp',
      url='https://bitbucket.org/cmscom/c2.search.kananormalizer',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['c2', 'c2.search'],
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
