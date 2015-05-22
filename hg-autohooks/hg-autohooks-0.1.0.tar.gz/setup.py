"""hg-autohooks setuptools information."""

import setuptools


setuptools.setup(
    name="hg-autohooks",
    version="0.1.0",
    description="Mercurial Autohooks Extension",
    author="Jon Ribbens",
    author_email="jon-hg-autohooks@unequivocal.co.uk",
    url="https://github.com/jribbens/hg-autohooks",
    license="GPLv2+",
    py_modules=["hgautohooks"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::"
            " GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Version Control",
    ],
)
