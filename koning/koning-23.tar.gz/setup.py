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
    version='23',
    url='https://pikacode.com/bthate/koning',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" KONING - niet de verboden maar de geboden vrucht. medicijnen eerst. """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["kern"],
    packages=['koning'],
    long_description=""" 

We moeten de Koning zien te overtuigen tot het strafbaar stellen van het toedienen van antipsychotica.

ARTIKEL 82 - INDIENEN WETSVOORSTEL

Voorstellen van wet kunnen worden ingediend door of vanwege de Koning en
door de Tweede Kamer der Staten-Generaal.

De Koning kan een voorstel van wet indienen die het toedienen van
antipsychotica strafbaar stelt. Het "Gij zult niet doden" moet de reden zijn dat het toedienen van 
antipsychotica strafbaar word gesteld, want antipsychotica brengen schade toe aan de hersens met 
dood tot gevolg.

Antipsychotica zijn dodelijk.

 """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
