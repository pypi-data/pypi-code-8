from . import graft
from contextlib import suppress
from uuid import getnode as get_mac
import locale
import netifaces
import os
import platform
import socket
import sys
try:
    from os import cpu_count
except ImportError:
    from multiprocessing import cpu_count


@graft
def cpu_info():
    """Returns cpu data.
    """
    return {
        'cpu_count': cpu_count()
    }


@graft
def os_info():
    """Returns os data.
    """
    return {
        'uname': dict(platform.uname()._asdict()),
        'path': os.environ.get('PATH', '').split(':'),
        'shell': os.environ.get('SHELL', '/bin/sh'),
    }


@graft
def python_info():
    """Returns Python data.
    """
    return {
        'python_version': '%s.%s.%s-%s%s' % sys.version_info,
        'python_executable': sys.executable,
        'python_path': sys.path
    }


@graft
def facts_info():
    """Returns facts library data.
    """
    from facts import __version__
    from . import __path__ as grafts_dirs
    return {
        'facts_version': __version__,
        'grafts_dirs': grafts_dirs
    }


@graft
def network_info():
    """Returns hostname, ipv4 and ipv6.
    """

    def extract(host, proto):
        return socket.getaddrinfo(host, None, proto)[0][4][0]
    host = socket.gethostname()
    response = {}
    response['hostname'] = host
    with suppress(IndexError):
        response['ipv4'] = extract(host, socket.AF_INET)
    with suppress(IndexError):
        response['ipv6'] = extract(host, socket.AF_INET6)
    return response


@graft
def mac_addr_info():
    """Returns mac address.
    """
    mac = get_mac()
    if mac == get_mac():  # not random generated
        hexa = '%012x' % mac
        value = ':'.join(hexa[i:i+2] for i in range(0, 12, 2))
    else:
        value = None
    return {'mac': value}


@graft
def locale_info():
    """Returns locale data.
    """
    code, encoding = locale.getdefaultlocale()
    return {
        'default_language': code,
        'default_encoding': encoding
    }


@graft
def interfaces_info():
    """Returns interfaces data.
    """
    def humanize(value):
        if value == netifaces.AF_LINK:
            return 'link'
        if value == netifaces.AF_INET:
            return 'ipv4'
        if value == netifaces.AF_INET6:
            return 'ipv6'
        return value

    results = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        results[iface] = {humanize(k): v for k, v in addrs.items()}

    return {
        'interfaces': results
    }


@graft
def gateways_info():
    """Returns gateways data.
    """
    data = netifaces.gateways()
    results = {'default': {}}

    with suppress(KeyError):
        results['ipv4'] = data[netifaces.AF_INET]
        results['default']['ipv4'] = data['default'][netifaces.AF_INET]
    with suppress(KeyError):
        results['ipv6'] = data[netifaces.AF_INET6]
        results['default']['ipv6'] = data['default'][netifaces.AF_INET6]

    return {
        'gateways': results
    }
