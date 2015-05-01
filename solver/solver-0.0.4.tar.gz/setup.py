import os

from setuptools import setup

setup(
    name = "solver",
    packages = ["solver.parsing", "solver.test"],
    version = "0.0.4",
    author = "Bahrom Matyakubov",
    author_email = "bahrom.matyakubov@gmail.com",
    url = "https://github.com/bahrom-matyakubov/solver",
    description = "Math problem solver",
    license = "MIT",
    long_description = open(os.path.join('README.rst')).read(),
    keywords = ["solver", "education", "mathematics"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)