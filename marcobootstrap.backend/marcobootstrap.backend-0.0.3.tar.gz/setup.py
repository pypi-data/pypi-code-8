#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The marco-bootstrap backend
"""
from setuptools import setup, find_packages
from codecs import open
import os, subprocess, glob, sys
from os.path import join

from distutils.command.clean import clean
from distutils.command.install import install
import stat

CERTIFICATES_DIR = "/etc/marcobootstrap/backend/certs"
SECRETS_DIR = "/etc/marcobootstrap/backend/"
STATIC_DIR = "/usr/lib/marcobootstrap/backend"

custom_marcobootstrap_backend_params = [
                                    "--marcobootstrap-no-daemons",
                                    "--marcoboostrap-no-start",]


def detect_init():
    """
    Detects the daemon management tool used in the system
    """
    try:
        subprocess.check_call(["systemctl", "--version"], 
                               stdout=None, 
                               stderr=None, 
                               shell=False)
        return 0
    except (subprocess.CalledProcessError, OSError):
        return 1


init_bin = detect_init()


def enable_service(service):
    """
    Enables the specified service using the existing service manager
    :param str service: The name of the service
    """
    sys.stdout.write("Enabling service "+service+"...")
    if init_bin == 0:
        subprocess.call(["systemctl", "enable", service], shell=False)
    else:
        subprocess.call(["update-rc.d", "-f", service, "remove"], shell=False)
        subprocess.call(["update-rc.d", service, "defaults"], shell=False)
    
    sys.stdout.write("Enabled!\n")

def start_service(service):
    """
    Starts the desired service using the existing service manager 
    :param str service: The name of the service
    """
    sys.stdout.write("Starting service " + service + "...")
    if init_bin == 0:
        subprocess.call(["systemctl", "start", service], shell=False)
    else:
        subprocess.call(["service", service, "start"], shell=False)

    sys.stdout.write("Started!\n")

def set_cert_permissions():
    """
    Sets the certificate permissions for the owner
    """
    for cert in os.listdir(CERTIFICATES_DIR):
        os.chmod(os.path.join(CERTIFICATES_DIR, cert), 
            stat.S_IREAD | stat.S_IWRITE)

    os.chmod(os.path.join(CERTIFICATES_DIR, "../secret"), 
                        stat.S_IREAD | stat.S_IWRITE)

    os.chmod(CERTIFICATES_DIR, 
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)

if __name__ == "__main__":
    marcobootstrap_params = []

    python_version = int(sys.version[0])

    marcobootstrap_params = [param for param in sys.argv\
                             if param in custom_marcobootstrap_backend_params]
    sys.argv = [arg for arg in sys.argv if arg not in marcobootstrap_params]

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
        long_description = f.read()

    data_files = [
                  ('/etc/marcobootstrap/backend/', ['etc/marcobootstrap/backend/backend.cfg'])
                 ]

    cert_files = [
                  (CERTIFICATES_DIR, 
                    glob.glob("etc/marcobootstrap/backend/certs/*"))
                 ]
    
    secret_files = [
                    (SECRETS_DIR, ["etc/marcobootstrap/backend/secret"])
                   ]

    static_files = [
                    (join(STATIC_DIR, "static/css"), glob.glob("usr/lib/marcobootstrap/backend/static/css/*")),
                    (join(STATIC_DIR, "static/fonts"), glob.glob("usr/lib/marcobootstrap/backend/static/fonts/*")),
                    (join(STATIC_DIR, "static/img"), glob.glob("usr/lib/marcobootstrap/backend/static/img/*")),
                    (join(STATIC_DIR, "static/js"), glob.glob("usr/lib/marcobootstrap/backend/static/js/*")),
                    (join(STATIC_DIR, "templates/"), glob.glob("usr/lib/marcobootstrap/backend/templates/*")),
                    (join(STATIC_DIR, "../tar"), glob.glob("usr/lib/marcobootstrap/backend/tar/*"))]


    if "--marcobootstrap-no-daemons" not in marcobootstrap_params:
        daemon_path = "daemon/"
        if init_bin == 1:
            daemon_files = [
                             ('/etc/init.d', 
                                [os.path.join(daemon_path, 
                                    "systemv/mbootstrapbackd")])
                           ]
        else:
            daemon_files = [
                            ('/etc/systemd/system', 
                                [os.path.join(daemon_path, 
                                "systemd/marcomanager.service")])
                           ]

        data_files.extend(daemon_files)
    
    data_files.extend(cert_files)
    data_files.extend(static_files)
    data_files.extend(secret_files)

    setup(
        name="marcobootstrap.backend",
        provides=["marcobootstrap.backend"],
        namespace_packages=['marcobootstrap'],
        version='0.0.3',
        description="The marcobootstrap utility",
        long_description=long_description,
        url="marcopolo.martinarroyo.net",
        author="Diego Martín",
        author_email="martinarroyo@usal.es",
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',

            'Topic :: System :: Boot',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',

            'Intended Audience :: System Administrators',

            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Natural Language :: English',
        ],
        keywords="pxe",
        packages=find_packages(),
        install_requires=[
            "certifi>=2015.4.28",
            "Django>=1.8.1",
            "passlib>=1.6.2",
            "pyjade>=3.0.0",
            "requests>=2.2.1",
            "requests-futures>=0.9.5",
            "six>=1.9.0",
            "tornado>=4.1",
            "pyopenssl",
            "ndg-httpsclient",
            "pyasn1"
        ],
        zip_safe=False,
        data_files=data_files,
        entry_points={
        'console_scripts':['mbootstrapbackd = marcobootstrap.backend.backend:main']
        }
    )
    if "install" in sys.argv:
        set_cert_permissions()

        if "--marcobootstrap-no-daemons" not in marcobootstrap_params:
            enable_service("mbootstrapbackd")
            start_service("mbootstrapbackd")

        if not os.path.exists("/var/log/marcopolo"):
            os.makedirs("/var/log/marcopolo")


