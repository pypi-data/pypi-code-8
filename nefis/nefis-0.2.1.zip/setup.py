from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import os
from distutils.core import setup
from distutils.extension import Extension
import numpy as np
try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = {}

ext_modules = []
if use_cython:
    ext_modules += [
        Extension("nefis.nefis",
                  ["nefis/nefis.pyx"],
                  libraries=["nefis"],
                  library_dirs=["./libs"],
                  include_dirs=[np.get_include()]
                  ),
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    print("Import failed (statement): 'from Cython.Distutils import build_ext'")

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Programming Language :: Python :: 2.7',
    'Operating System :: Microsoft :: Windows',
]

# define package data
packageData = []
for fileName in os.listdir(os.path.join(".", "data")):
    name, ext = os.path.splitext(fileName)
    packageData.append("data/%s" % fileName)
packageData.append("libs/nefis.dll" )
packageData.append("libs/msvcr110.dll" )

packageTests = []
for fileName in os.listdir(os.path.join(".", "tests")):
    name, ext = os.path.splitext(fileName)
    packageTests.append("tests/%s" % fileName)

setup(
# https://packaging.python.org/en/latest/distributing.html#setup-args
    name='nefis',
    version='0.2.1',
    description='NEFIS library',
    long_description=long_description,
    url='http://oss.deltares.nl/web/delft3d',
    author='Jan Mooiman',
    author_email='jan.mooiman@deltares.nl',
    license='LGPLv3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=classifiers,
    keywords='nefis file_format',
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    data_files=[('', packageData)],
    packages=find_packages(),
    test_suite="tests"
)
