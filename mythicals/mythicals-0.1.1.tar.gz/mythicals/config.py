import os
import platform
import socket
import sys

import netaddr


HOST_NAME = socket.gethostname()

# http://stackoverflow.com/a/8208857
if platform.dist()[0].lower() == 'ubuntu':
    DATA_PREFIX = os.path.join(sys.prefix, 'local', 'mythicals')
else:
    DATA_PREFIX = os.path.join(sys.prefix, 'mythicals')

DB = {
    'url': 'postgresql://mythical:mythical@localhost/mythical',
    'kwargs': {
        'echo': False,
    }
}

DOWNLOADS = {
    'use': 'os',
    'os': {
        'root': '/tmp/mythical'
    },
    's3': {
        'bucket': 'verygood-mythical',
        'prefix': 'dev',
        'aws_access_key': None,
        'aws_secret_key': None,
    },
}

UPLOADS = {
   'root': '/tmp/mythical',
}

NEWRELIC = {
    'config_file': None,
    'environment': 'dev',
}

# api

API_HEADERS = {
    'trace_id': 'X-VG-Trace',
    'user_id': 'X-Mythical-User-Id'
}

API_ALLOWED_CIDRS = [
    netaddr.IPNetwork('127.0.0.1'),
]

API_HEALTH = {
    'file_path': None,
}

API_PROXIED = False

API_RECORD = False

API_NEWRELIC = False

# sftp

SFTP_PROXY_CIDRS = [
    netaddr.IPNetwork('10/8'),
    netaddr.IPNetwork('127.0.0.1'),
]
