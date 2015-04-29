from setuptools import setup, find_packages
import os

version = '0.1.0'

setup(name='c2.splitter.janome',
      version=version,
      description="This product is split word by janome for Plone.",
      long_description=open("README.rst").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone splitter',
      author='Manabu TERADA, Hajime Nakagami',
      author_email='terada@cmscom.jp, nakagami@gmail.com',
      url='https://github.com/nakagami/c2.splitter.janome',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['c2', 'c2.splitter'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'janome',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
