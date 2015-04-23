__author__ = 'chb'

from distutils.core import setup
from distutils.extension import Extension


setup(
  name = 'pyqlz',
  version='1.5.0',
  ext_modules=[
    Extension("pyqlz", 
		     ["pyqlz.c"],
		     extra_compile_args=['-std=c99'])]
)