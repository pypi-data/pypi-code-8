from __future__ import absolute_import
from collections import OrderedDict

import logging
import os
import pkg_resources
import socket
import subprocess
import sys
import urllib

from conversion.boolean import convert_bool

from .config import API_URL, get_config
from .websocket import websocket


WEBSOCKET_URL = os.environ.get('WEBSOCKET_URL', 'wss://ws.zymbit.com/channel')
SSL_CHECK_HOSTNAME = convert_bool(os.environ.get('SSL_CHECK_HOSTNAME', 'true'))


def find_cpuinfo(markers):
    # no support for non-linux systems
    if os.path.exists('/proc/cpuinfo'):
        content = open('/proc/cpuinfo', 'rb').read()
        for marker, return_value in markers.items():
            if marker in content:
                return return_value


def get_api_url(path):
    _config = get_config()
    api_url = _config.get('cloud', {}).get('api_url', API_URL)

    return '{}{}'.format(api_url, path)


def get_connection(url=None, credentials=None, check_hostname=None):
    headers = []

    logger = logging.getLogger(__name__)

    if check_hostname is None:
        check_hostname = SSL_CHECK_HOSTNAME

    sslopt = {"check_hostname": check_hostname}

    url = url or WEBSOCKET_URL
    request_url = url
    if credentials:
        connector_version = pkg_resources.require('zymbit')[0].version

        credentials.update({
            'hostname': socket.gethostname(),
            'connector_version': connector_version,
        })

        credentials.update(get_device_meta())

        encoded = urllib.urlencode(credentials)
        request_url = '{}?{}'.format(url, encoded)

    logger.debug('getting websocket connection at url={}'.format(url))

    ws = websocket.create_connection(request_url, header=headers, sslopt=sslopt)
    ws.settimeout(0)

    return ws


def get_device_meta():
    device_meta = {}

    try:
        # TODO: support linux
        # this didn't work on a server container, so just removed this altogether
        # because these params are intended for additional device metadata, but it
        # would be great to be able to get this from any system.
        from .compat import util
    except ImportError:
        pass
    else:
        device_meta.update({
            'distro': util.get_distro(),
            'model': util.get_model(),
            'system': util.get_system(),
        })

    return device_meta


def get_model():
    systems = OrderedDict((
        ('Arduino Yun', 'yun'),
        ('BCM2708', '1'),
        ('BCM2709', '2'),
    ))
    cpuinfo = find_cpuinfo(systems)
    if cpuinfo:
        return cpuinfo

    if sys.platform == 'darwin':
        return sys.platform


def get_system():
    systems = OrderedDict((
        ('Arduino Yun', 'arduino'),
        ('BCM270', 'raspberrypi'),  # note this will match BCM2708 (rpi) and BCM2709 (rpi2)
    ))
    cpuinfo = find_cpuinfo(systems)
    if cpuinfo:
        return cpuinfo

    if sys.platform == 'darwin':
        return sys.platform


def run_command(command):
    return subprocess.Popen(command).wait()
