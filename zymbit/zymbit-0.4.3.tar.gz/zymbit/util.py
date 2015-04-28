from __future__ import absolute_import

import logging
import os
import subprocess
import sys
import urllib

from conversion.boolean import convert_bool

from .config import API_URL, get_config
from .websocket import websocket


WEBSOCKET_URL = os.environ.get('WEBSOCKET_URL', 'wss://ws.zymbit.com/channel')
SSL_CHECK_HOSTNAME = convert_bool(os.environ.get('SSL_CHECK_HOSTNAME', 'true'))


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
        encoded = urllib.urlencode(credentials)
        request_url = '{}?{}'.format(url, encoded)

    logger.debug('getting websocket connection at url={}'.format(url))

    ws = websocket.create_connection(request_url, header=headers, sslopt=sslopt)
    ws.settimeout(0)

    return ws


def get_system():
    # no support for non-linux systems
    if os.path.exists('/proc/cpuinfo'):
        content = open('/proc/cpuinfo', 'rb').read()
        if 'Arduino Yun' in content:
            return 'arduino'
        elif 'BCM270' in content:  # note this will match BCM2708 (rpi) and BCM2709 (rpi2)
            return 'raspberrypi'

    if sys.platform == 'darwin':
        return sys.platform


def run_command(command):
    return subprocess.Popen(command).wait()
