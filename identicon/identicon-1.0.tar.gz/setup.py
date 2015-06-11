import os
from setuptools import setup

setup(
  name='identicon',
  version='1.0',
  py_modules=['identicon'],
  license='BSD',
  description='identicon python implementation',
  long_description='identicon python implementation',
  url='https://github.com/shnjp/identicon',
  author='Shin Adachi',
  author_email='shn@glucose.jp',
  install_requires=["Pillow"],
)
