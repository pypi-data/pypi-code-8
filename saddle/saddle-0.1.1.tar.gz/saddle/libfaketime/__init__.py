import os
import sys


__version__ = "0.9.6"
LIBFAKETIME_DIR = os.path.dirname(os.path.realpath(__file__))


def get_environment_vars(filename):
    """Return a dict of environment variables required to run a service under faketime."""
    if sys.platform == "linux" or sys.platform == "linux2":
        return {
            'LD_PRELOAD':  LIBFAKETIME_DIR + os.sep + "libfaketime.so.1",
            'FAKETIME_SKIP_CMDS': 'nodejs',
            'FAKETIME_TIMESTAMP_FILE': filename,
        }
    elif sys.platform == "darwin":
        return {
            'DYLD_INSERT_LIBRARIES': LIBFAKETIME_DIR + os.sep + "libfaketime.1.dylib",
            'DYLD_FORCE_FLAT_NAMESPACE': '1',
            'FAKETIME_TIMESTAMP_FILE': filename,
        }
    else:
        raise RuntimeError("libfaketime does not support '{}' platform".format(sys.platform))
