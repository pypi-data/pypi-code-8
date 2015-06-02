# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='primarycolors',
      version='0.4',
      description='Determination of the primary colors in an image file.',
      author='Rodion S.',
      author_email='python@profserver.ru',
      url='https://pypi.python.org/pypi/primarycolors/',
      license='GPL',
      platforms=('Linux', 'MacOS X'),
      keywords = ('clustering', 'colors', 'primary colors', 'k-means'),
      packages=['primarycolors'],
      package_dir={'primarycolors': 'src/primarycolors'},
      requires=['scipy', 'numpy', 'Pillow', 'six'],
      install_requires=['scipy', 'numpy', 'Pillow', 'six'],
      classifiers = [
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
          "Environment :: Console",
          'Operating System :: MacOS',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4", ]
      )
