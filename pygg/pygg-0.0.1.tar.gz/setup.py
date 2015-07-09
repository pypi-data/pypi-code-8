#!/usr/bin/env python2.7
try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
from setuptools import setup, find_packages
import pyplot

setup(name="pygg",
      version=pyplot.__version__,
      description="ggplot2 syntax for python.  Runs R's version of ggplot2 under the covers",
      license="MIT",
      author="Eugene Wu",
      author_email="ewu@cs.columbia.edu",
      url="http://github.com/sirrice/pyplot",
      packages = find_packages(),
      include_package_data = True,      
      package_dir = {'pyplot' : 'pyplot'},
      scripts = [
        'bin/runpyplot.py'
      ],
      install_requires = [
        'click'
      ],
      keywords= "")
