from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='pyodcompare',
      version=version,
      description="Generate a comparaison of two libreoffice documents using uno",
      long_description="""\
Use libreoffice compare feature to generate an openoffice document with modifications registered from two versions of a document""",
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7"]
      , # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='libreoffice openoffice',
      author='Thomas Desvenain',
      author_email='thomas.desvenain@gmail.com',
      url='https://github.com/IMIO/pyodcompare',
      license='GPL v3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      test_suite="pyodcompare.tests",
      entry_points = {
        'console_scripts': ['pyodcompare=main:execute'],
      },
      extras_require={
        'test': [
            'PyODConverter',
        ],
      },
      )
