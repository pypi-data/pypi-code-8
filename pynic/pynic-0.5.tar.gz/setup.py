from setuptools import setup, Extension
import os

PYNIC_VERSION = '0.5'

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: C",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]
 
module = Extension('pynic',
                    define_macros = [('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '5')], 
                    sources = ['pynic/pynic.c', 'pynic/iface.c'])
 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = 'pynic',
      version = PYNIC_VERSION,
      description = 'It is an interface to get NIC information',
      author = 'Alfredo Miranda',
      author_email = 'alfredocdmiranda@gmail.com',
      url = 'https://github.com/alfredocdmiranda/pynic',
      keywords="NIC network interface",
      license='GPLv3',
      long_description=read('DESCRIPTION.rst'),
      classifiers=CLASSIFIERS,
      ext_modules = [module])
