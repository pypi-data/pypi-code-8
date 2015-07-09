#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
import os
from distutils.core import setup
from distutils.command.clean import clean
from distutils.command.install import install
import os, sys
import subprocess

custom_marcopolomanager_params = [
                            "--marcopolomanager-disable-daemons",
                             ]

def detect_init():
    try:
        subprocess.check_call(["systemctl", "--version"], stdout=None, stderr=None, shell=False)
        return 0
    except (subprocess.CalledProcessError, OSError):
        return 1

init_bin = detect_init()

def enable_service(service):
    sys.stdout.write("Enabling service " + service +"...")
    if init_bin == 0:
        subprocess.call(["systemctl", "enable", service], shell=False)
    else:
        subprocess.call(["update-rc.d", "-f", service, "remove"], shell=False)
        subprocess.call(["update-rc.d", service, "defaults"], shell=False)
    
    sys.stdout.write("Enabled!")

def start_service(service):
    sys.stdout.write("Starting service " + service + "...")
    if init_bin == 0:
        subprocess.call(["systemctl", "start", service], shell=False)
    else:
        subprocess.call(["service", service, "start"], shell=False)

    sys.stdout.write("Started!")

if __name__ == "__main__":
    
    marcopolomanager_params = [param for param in sys.argv if param in custom_marcopolomanager_params]
    
    sys.argv = [param for param in sys.argv if param not in marcopolomanager_params]

    python_version = int(sys.version[0])

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as description_f:
        long_description = description_f.read()

    data_files = [
                  ('/etc/marcopolomanager/', ["etc/marcopolomanager/marcopolomanager.cfg", os.path.join(here, "etc/marcopolomanager/__init__.py")]),
                  ('/etc/marcopolomanager/managers/', [os.path.join(here, "etc/marcopolomanager/managers/managers.py"),
                                                   os.path.join(here, "etc/marcopolomanager/managers/__init__.py")])
                 ]

    if "--marcopolomanager-disable-daemons" not in marcopolomanager_params:
        

        if init_bin == 1:
            daemon_files = [
                         ('/etc/init.d/', ["daemons/systemv/marcopolomanagerd"])
                       ]
        else:
            daemon_files = [('/etc/systemd/system/',["daemons/systemd/marcopolomanager.service"])]

        data_files.extend(daemon_files)

    install_requires = ["marcopolo>=0.1.0",
                        "tornado>=4.1",
                        "certifi>=2015.4.28"
                       ]

    if python_version == 2:
        install_requires.append("futures>=3.0.3")

    setup(
        name="marcopolo-manager",
        provides=["marcopolomanager"],
        version='0.1.1',
        description="A task scheduler with MarcoPolo integration",
        long_description=long_description,
        url="marcopolo.martinarroyo.net",
        author="Diego Martín",
        author_email='martinarroyo@usal.es',
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',

            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4','Development Status :: 3 - Alpha',

            'Intended Audience :: System Administrators',

            'Topic :: Software Development :: Build Tools',
            'Topic :: System :: Networking',
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

            'Natural Language :: English',

        ],

        keywords="marcopolomanager task scheduler",
        packages=find_packages(),
        install_requires=install_requires,
        zip_safe=False,
        data_files=data_files,
        entry_points={
            'console_scripts':["marcopolomanagerd = marcopolomanager.runner:main",
                                "marcopolomanagerreload = marcopolomanager.marcopolomanagerreload:main"
                              ]
        }
    )
    if "install" in sys.argv:    
        if "--marcopolomanager-disable-daemons" not in marcopolomanager_params:
            enable_service("marcopolomanagerd")
            start_service("marcopolomanagerd")