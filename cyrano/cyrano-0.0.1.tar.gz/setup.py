import os
from distutils.core import setup

install_requires = []

with open(os.path.join('cyrano', '_version.py'), 'r') as inp:
    _, VERSION = inp.read().split("=")
    VERSION = VERSION.strip(' "\n')

setup(
    name="cyrano",
    author="Sasha Hart",
    version=VERSION,
    url="http://github.com/sashahart/cyrano",
    author_email="s@sashahart.net",
    packages=["cyrano"],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
    ],
)
