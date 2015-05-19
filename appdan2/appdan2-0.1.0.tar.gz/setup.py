from distutils.core import setup

setup(
    # Application name:
    name="appdan2",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="dmbugua",
    author_email="danmbugua74@gmail.com",

    # Packages
    packages=["appdan2"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://testpypi.python.org/pypi/appdan2_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)
