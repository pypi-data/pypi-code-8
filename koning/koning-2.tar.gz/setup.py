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
    version='2',
    url='https://pikacode.com/bthate/koning',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" Behandeling met antipsychotica zonder de noodzakelijke verpleging is maken van omstandigheden die suicide in de hand werken. """,
    license='MIT',
    include_package_data=True,
    zip_safe=True,
    install_requires=["wet", ],
    scripts=["bin/koning", ],
    packages=['koning',
             ],
    long_description=""" 

Antipsychotica zijn dodelijke medicijnen en daarom is verpleging een
noodzaak. Behandeling met antipsychotica zonder de noodzakelijke verpleging
is maken van omstandigheden die suicide in de hand werken.

(F)ACT bied niet de noodzakelijke verpleging die behandeling met
antipsychotica verantwoord maken.

1) verpleging naar gelang de situatie - meer zorg naarmate de situatie erger is, is niet preventief.
2) niet 7 x 24 uurs verpleging - in het weekend en avonduren niet aanwezig  
3) psychiater is niet op de hoogte van de situatie van de patient
4) behandelovereenkomsten zijn niet volledig
5) zonder bedden geen snelle terugbrenging naar ziekenhuis mogelijk.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
