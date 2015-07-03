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
    version='27',
    url='https://pikacode.com/bthate/koning',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" KONING - niet de verboden maar de geboden vrucht. medicijnen eerst. """,
    license='MIT',
    zip_safe=False,
    install_requires=["kern"],
    packages=['koning'],
    long_description=""" 

Behandelen met antispsychotica is mishandeling met dood tot gevolg.

Titel XX. Mishandeling

Artikel 300 

1. Mishandeling wordt gestraft met gevangenisstraf van ten hoogste drie jaren of geldboete van de vierde categorie. 
2. Indien het feit zwaar lichamelijk letsel ten gevolge heeft, wordt de schuldige gestraft met gevangenisstraf van ten hoogste vier jaren of geldboete van de vierde categorie. 
3. Indien het feit de dood ten gevolge heeft, wordt hij gestraft met gevangenisstraf van ten hoogste zes jaren of geldboete van de vierde categorie. 
4. Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid. 
5. Poging tot dit misdrijf is niet strafbaar.

304. De in de artikelen 300-303 bepaalde gevangenisstraffen kunnen met een derde worden verhoogd

3°. indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

 """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
