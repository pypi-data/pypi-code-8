from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='SimpleWebDav',
    version='0.1',
    description = "Simple WebDav library",
	author = "Kosmachev Alex",
	author_email = "adkosmachev@edu.hse.ru",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'mutagen'
    ]
)