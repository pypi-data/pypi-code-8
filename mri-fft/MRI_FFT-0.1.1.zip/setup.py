__author__ = 'Tom'

import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "MRI_FFT",
    version = "0.1.1",
    author = "Thomas Bealing",
    author_email = "thomasbealing@gmail.com",
    description = ("Optimized functions for performing 1D, 2D and 3D "
                        "inverse Fourier's transforms, using Reikna and FFTW"),
    license = "GPL-3",
    keywords = "MRI FFT iFFT Reikna FFTW",
    long_description = read('README.txt'),
    url = "https://www.dropbox.com/sh/tsjhzubwm0k5o9j/AABIBwPLRJG6gvN9WeBZv4JMa?dl=0",
    packages = ['MRI_FFT'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)