# -*- coding: utf-8 -*-

import os
from setuptools import setup

LOCALES = [
    ('default.py', 'gaminator'),
]

PACKAGES = [
    '%s',
    '%s.starter',
]

DESCRIPTION = """A library for easy and fast development of simple games.
For educational purposes.
"""

def get_packages():
    for _, dest_root in LOCALES:
        for package in PACKAGES:
            yield package % dest_root

setup(
    name="gaminator",
    version="0.1.0",
    author=u"Marián Horňák",
    author_email="marian.sysel.hornak@gmail.com",
    description=DESCRIPTION,
    license="MIT",
    keywords=["education", "game"],
    url="https://github.com/syslo/gaminator",
    download_url="https://github.com/syslo/gaminator/tarball/v0.1.0",
    packages=list(get_packages()),
    classifiers=[
        "Development Status :: 4 - Beta",
    ],
)
