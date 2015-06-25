from . import graft

import socket
import platform
import sys
try:
    from os import cpu_count
except ImportError:
    from os import cpu_count


@graft
def cpu_core():
    return {
        'cpu_count': cpu_count()
    }


@graft
def os_name():
    return {
        'uname': dict(platform.uname()._asdict())
    }


@graft
def python():
    return {
        'python_version': '%s.%s.%s-%s%s' % sys.version_info,
        'python_executable': sys.executable
    }


@graft
def facts():
    from facts import __version__
    from . import __path__ as grafts_dirs
    return {
        'facts_version': __version__,
        'grafts_dirs': grafts_dirs
    }


@graft
def network():
    hostname = socket.gethostname()
    ipv4 = socket.gethostbyname(hostname)
    return {
        'hostname': hostname,
        'ipv4': ipv4
    }
