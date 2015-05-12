import os
from setuptools import setup, find_packages

from machinepack import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="machinepack",
    version=__version__,
    author="Maciej Kucharz",
    author_email="maciej.kucharz@syncano.com",
    description="Toolkit for Python machinepacks",
    license="MIT",
    keywords="machinepack tools packages",
    url="http://python-machine.org",
    packages=find_packages(),
    include_package_data = True,
    entry_points={
        'console_scripts': ['pymachine=machinepack.command_line:cli'],
    },
    install_requires=[
        'click',
        'mako',
        'coverage',
        'colorama',
        'pygments',
        'mock',
        'six',
        'nose',
        'pylint',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
