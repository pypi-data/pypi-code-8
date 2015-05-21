import os
from setuptools import setup, find_packages

version = '0.2.5'

description = "Unoffical Project Free TV API"

cur_dir = os.path.dirname(__file__)

setup(
        name = "project-free-tv",
        version = version,
        url = "https://github.com/gnijuohz/Project-Free-TV-API",
        author='Jing Zhou',
        author_email='gnijuohz@gmail.com',
        license = "MIT",
        description = description,
        packages = ['freetv'],
        install_requires = ['setuptools', 'lxml', 'requests', 'youtube-dl'],
        )
