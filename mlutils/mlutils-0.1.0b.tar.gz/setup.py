#!/usr/bin/env python

from distutils.core import setup

description = """ Collection of utilities for AI planning and not-supervised learning. Development is in progress. """

long_description = """
mlutils package is intended to be a collection of utilities for AI planning and not-supervised learning. 
Development is in progress.

Version history:

0.1.0
  -- N-Ary tree class supported various search algorithms: pre-order, post-order, breadth-first, 
     heuristic (you should provide heuristic function) and random sampling 
  -- State space generation/search   

Next version:
   Supposed to provide streaming clustering algorithm
"""

classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: BSD License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',   
],

setup(
      name = "mlutils",
      version = "0.1.0b",
      description = description,
      long_description=long_description,
      author = "Mark Eremeev",
      author_email = "m.eremeev@gmail.com",
      license = "BSD",
      url = "https://gitlab.com/m.eremeev/mlutils",
      packages=["mlutils"],    
      py_modules=["mlutils_usage"],
      keywords = "machine learning, decision tree search, AI planning",
    )
