from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='mpa',
	version = "0.1.1b1",
	description="Matplotlib Plotting Assistant",
    long_description=long_description,
	url="https://github.com/yuhangwang/MPA",
	author="Yuhang Wang",
	license="BSD 3-Clause License",
	packages = find_packages(),
      )