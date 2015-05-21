from setuptools import setup, find_packages
import synergine_lifegame

setup(
    name='synergine_lifegame',
    version='0.0.1.5',
    packages=find_packages(),
    install_requires=['synergine', 'synergine_xyz'],
    author='Bastien Sevajol',
    author_email="synergine@bux.fr",
    description='Synergy howto project',
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://github.com/buxx/synergine-lifegame',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ]
)