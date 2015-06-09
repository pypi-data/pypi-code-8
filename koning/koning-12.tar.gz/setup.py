#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run KONING with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='koning',
    version='12',
    url='https://pikacode.com/bthate/koning',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" Nieuwe Grondwet """,
    license='MIT',
    include_package_data=True,
    zip_safe=True,
    install_requires=["wet", ],
    scripts=["bin/koning", ],
    packages=['koning',
             ],
    long_description=""" Nieuwe grondwet ter strafbaar stelling van het plegen van een oordeel dat een enkel persoon betreft.

De hel die het persoonlijk oordeel bij de mens brengt, laat Gods eigen
schepping in de Hel branden.

Niet een heilige geest die de mens goed maakt, maar een Heilige Geest die de 
wereld goed maakt.

Niet de persoon moet zich aanpassen, de maatschappij moet zich aanpassen.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
