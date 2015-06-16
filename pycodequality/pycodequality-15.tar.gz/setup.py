# coding=utf-8
"""
author  : rabshakeh (erik@a8.nl)
project : pycodequality
created : 26-05-15 / 15:00
"""
from setuptools import setup

setup(name='pycodequality',
      version='15',
      description='Pylint measures code quality for every file in the folder, returns an average',
      url='https://github.com/erikdejonge/pycodequality',
      author='Erik de Jonge',
      author_email='erik@a8.nl',
      license='GPL',
      packages=['pycodequality'],
      entry_points={
          'console_scripts': [
              'pcq=pycodequality:main',
          ],
      },
      zip_safe=True,
      install_requires=['pylint', 'pylint-django', 'cmdssh'],
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta ",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: POSIX",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Terminals",
          "Topic :: System",
      ])
