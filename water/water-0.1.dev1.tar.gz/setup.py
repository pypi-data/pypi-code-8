from setuptools import setup

setup(
  name='water',
  version='0.1.dev1',
  packages=['water'],
  description='Apply watermarks to images',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4'
  ],
  install_requires=['Pillow==2.8.2'],
)
