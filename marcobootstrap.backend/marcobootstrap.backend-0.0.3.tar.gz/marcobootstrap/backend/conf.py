# -*- coding: utf-8 -*-
from os.path import dirname, join, isabs
import logging
import six
from six.moves import configparser

CONF_DIR = "/etc/marcobootstrap/backend/"

directory = dirname(__file__)
cert_dir = "/etc/marcobootstrap/backend/certs"

certs = join(directory, cert_dir)

APPCERT = join(certs, "app.crt")
APPKEY  = join(certs, "app.key")

RECEIVERCERT = join(certs, "receiver.crt")
RECEIVERKEY = join(certs, "receiver.key")

BACKEND_FILES_PORT = 1345
BACKEND_PORT= 1346
NON_SECURE_BACKEND_PORT = 1445
SLAVE_PORT = 1360

ADMIN = "admin"
ADMIN_PASS = '$5$rounds=110000$H6PevFw6VZ.IiUqL$beL6q6C9R6dVqFUQLtWsHYzXyOqoqBYOa13Z1lR5Z.1'
DB_FILE="/etc/marcobootstrap/scheduled.db"

LOG_FILE = "/var/log/marcopolo/marcobootstrapbackendd.log"
COOKIE_SECRET_FILE = "/etc/marcobootstrap/backend/secret"

TAR_PATH = "/etc/marcobootstrap/backend/tar"
BOOTCODE_PATH = "/etc/marcobootstrap/backend/bootcode"
STATIC_PATH = "/usr/lib/marcobootstrap/backend/static"
TEMPLATES_DIR = "/usr/lib/marcobootstrap/backend/templates"

SERVICE_NAME= "marcobootstrap"

default_values={
    'directory':directory,
    'cert_dir':cert_dir,
    'certs':certs,
    'APPCERT':APPCERT,
    'APPKEY ':APPKEY ,
    'RECEIVERCERT':RECEIVERCERT,
    'RECEIVERKEY':RECEIVERKEY,
    'STATIC_PATH':STATIC_PATH,
    'BACKEND_FILES_PORT':BACKEND_FILES_PORT,
    'BACKEND_PORT':BACKEND_PORT,
    'SLAVE_PORT':SLAVE_PORT,
    'ADMIN':ADMIN,
    'ADMIN_PASS':ADMIN_PASS,
    'DB_FILE':DB_FILE,
    'LOG_FILE':LOG_FILE,
    'COOKIE_SECRET_FILE':COOKIE_SECRET_FILE,
    'TAR_PATH':TAR_PATH,
    'BOOTCODE_PATH':BOOTCODE_PATH,
    'STATIC_PATH':STATIC_PATH,
    'TEMPLATES_DIR':TEMPLATES_DIR,
    'DB_FILE':DB_FILE,
    'SERVICE_NAME':SERVICE_NAME,
    'NON_SECURE_BACKEND_PORT':NON_SECURE_BACKEND_PORT
}

config = configparser.RawConfigParser(default_values, allow_no_value=False)

BACKEND_FILE_READ = join(CONF_DIR, 'backend.cfg')

try:
    with open(BACKEND_FILE_READ, 'r') as df:
        config.readfp(df)
        
        directory = config.get('backend', 'directory')
        cert_dir = config.get('backend', 'cert_dir')
        certs = config.get('backend', 'certs')
        
        APPCERT = config.get('backend', 'APPCERT')
        APPCERT = APPCERT if isabs(APPCERT) else join(certs, APPCERT)
        
        APPKEY  = config.get('backend', 'APPKEY')
        APPKEY = APPKEY if isabs(APPKEY) else join(certs, APPKEY)
        
        RECEIVERCERT = config.get('backend', 'RECEIVERCERT')
        RECEIVERCERT = RECEIVERCERT if isabs(RECEIVERCERT) else join(certs, RECEIVERCERT)
        
        RECEIVERKEY = config.get('backend', 'RECEIVERKEY')
        RECEIVERKEY = RECEIVERKEY if isabs(RECEIVERKEY) else join(certs, RECEIVERKEY)
        
        STATIC_PATH = config.get('backend', 'STATIC_PATH')
        BACKEND_FILES_PORT = config.getint('backend', 'BACKEND_FILES_PORT')
        BACKEND_PORT = config.getint('backend', 'BACKEND_PORT')
        SLAVE_PORT = config.getint('backend', 'SLAVE_PORT')
        ADMIN = config.get('backend', 'ADMIN')
        ADMIN_PASS = config.get('backend', 'ADMIN_PASS')
        DB_FILE = config.get('backend', 'DB_FILE')
        LOG_FILE = config.get('backend', 'LOG_FILE')
        COOKIE_SECRET_FILE = config.get('backend', 'COOKIE_SECRET_FILE')
        TAR_PATH = config.get('backend', 'TAR_PATH')
        BOOTCODE_PATH = config.get('backend', 'BOOTCODE_PATH')
        TEMPLATES_DIR = config.get('backend', 'TEMPLATES_DIR')
        SERVICE_NAME = config.get('backend', 'SERVICE_NAME')
        NON_SECURE_BACKEND_PORT = config.get('backend', 'NON_SECURE_BACKEND_PORT')

except IOError as i:
    logging.warning("Warning! The configuration file could not be read. Defaults will be used as fallback")
except Exception as e:
    logging.warning("Unknown exception in configuration parser: %s" % e)