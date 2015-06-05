from setuptools import setup

setup(
    # Application name:
    name="MillisecondCounter",

    # Version number (initial):
    version="0.0.1",

    # Application author details:
    author="Stuart Munro",
    author_email="stuart@munro.co",

    # Packages
    packages=["MillisecondCounter"],

    # Details
    url="https://github.com/stuartornum/python-MillisecondCounter",

    #
    # license="LICENSE.txt",
    description="Python utility class to get execution runtime in milliseconds",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[],

    license = "MIT",

    platforms = "Posix; MacOS X",

    classifiers = ["Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Topic :: Internet"],
)