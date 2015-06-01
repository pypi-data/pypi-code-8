from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

from Cython.Build import cythonize

import numpy

setup(name='COS',
      version='0.1.0',
      packages=find_packages(),
      description='Utilities for data taken with the Cosmic Origins '
                  'Spectrograph on the Hubble Space Telescope',
      setup_requires=['cython'],
      install_requires=['astropy>=1.0', 'scipy', 'matplotlib'],
      author='Charles Finn',
      author_email='c.w.finn2301@gmail.com',
      license='BSD',
      url='https://github.com/cwfinn/COS',
      download_url='https://pypi.python.org/pypi/COS/0.1.0',
      classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Cython',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics'
      ],
      provides=['COS'],
      zip_safe=False,
      use_2to3=False,
      entry_points={
          'console_scripts': [
              'runcalcos = COS.reduction:main'
          ]
      },
      ext_modules=cythonize('COS/_convolve.pyx'),
      include_dirs=[numpy.get_include(), ],
      include_package_data=True
      )
