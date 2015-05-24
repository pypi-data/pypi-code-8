#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="trust",
    version="1.0.4",
    description="A hierarchical database engine with read-only access to "
                "data, ideally used for cross-application settings and "
                "infrastructure description.",
    long_description=open("README.markdown").read(),
    author="Arseni Mourzenko",
    author_email="arseni.mourzenko@pelicandd.com",
    url="http://go.pelicandd.com/n/python-trust",
    license="MIT",
    keywords="database json settings",
    install_requires=[
        "markdown==2.6.1",
        "passlib==1.6.2"
    ],
    packages=["trust"],
    # Since it seems that there is no way to include data with `data_files`,
    # this looks like the only way to include the deployment script and other
    # static files. Since the name of the package is mandatory, any name which
    # exists in the project will work.
    package_data={
        "trust": [
            "../local.py",
            "../server.py",
            "../extras/*"
        ]
    }
)
