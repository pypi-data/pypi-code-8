import os
import shutil
import tempfile
import logging

from django.conf import settings
import importlib


LOGGER = logging.getLogger(__name__)


class BackendAdapter(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def put(self, dest, file):
        raise NotImplementedError()


class LocalFSAdapter(BackendAdapter):
    """A publisher backend adapter that copies files to a directory on the local
    machine.

    The ``BACKEND_ADAPTER_ARGS`` setting must have the field ``fs_root`` set to
    the path of the root directory (e.g. /tmp/blah_dir/).

    """
    def put(self, dest, file):
        assert 'fs_root' in self.kwargs

        if not os.path.isdir(self.kwargs['fs_root']):
            os.makedirs(self.kwargs['fs_root'], 0o774)

        tmp = tempfile.NamedTemporaryFile()
        # In this case `file' is actually a bytestring!
        # Tempfiles have to be rewound to be written/copied
        tmp.write(file)
        tmp.seek(0)

        file_dest = os.path.join(self.kwargs['fs_root'], dest)
        dest_dir = os.path.dirname(file_dest)

        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir, 0o774)

        try:
            shutil.copyfile(os.path.abspath(tmp.name), file_dest)
            tmp.close()
        except Exception as err:
            LOGGER.exception(err)
            return None

        return file_dest


def get_adapter():
    adapter = settings.BACKEND_ADAPTER
    module_name = ".".join(adapter.split('.')[:-1])
    m = importlib.import_module(module_name)
    klass = getattr(m, adapter.split('.')[-1])

    return klass(None, **settings.BACKEND_ADAPTER_ARGS)
