import os

from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name = "solver",
    packages = ["solver.arithmetic", "solver.parsing", "solver.test"],
    version = "0.0.3",
    author = "Bahrom Matyakubov",
    author_email = "bahrom.matyakubov@gmail.com",
    url = "https://github.com/bahrom-matyakubov/solver",
    description = "Math problem solver",
    long_description = (read('README.rst') + '\n\n' +
                        read('HISTORY.rst') + '\n\n'),
    keywords = ["solver", "education", "mathematics"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)