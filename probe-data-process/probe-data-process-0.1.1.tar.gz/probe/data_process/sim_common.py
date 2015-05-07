from __future__ import absolute_import
import h5py
import logging
import sys

cfg = {'debug': 3}


class MultiLineFormatter(logging.Formatter):

    def __init__(self, fmt, datefmt):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        # hack: http://stackoverflow.com/a/5879524/533618
        backup_exc_text = record.exc_text
        record.exc_text = None
        formatted = logging.Formatter.format(self, record)
        header = formatted.split(record.message)[0]
        record.exc_test = backup_exc_text
        return header + ('\n' + header).join(it for it in record.message.split('\n') if it)


logger = logging.getLogger()
logger.setLevel({1: logging.WARNING,
                 2: logging.INFO,
                 3: logging.DEBUG}.get(cfg['debug'], 0))
sh = logging.StreamHandler(sys.stderr)
fmt = '%(asctime)s.%(msecs).03d %(process)+5s %(levelname)-8s %(filename)s:%(lineno)d:%(funcName)s(): %(message)s'
sh.setFormatter(MultiLineFormatter(fmt, '%Y-%m-%d %H:%M:%S'))
logger.handlers = []
logger.addHandler(sh)


class SimCommon(object):
    """
    This is a simple "low-level" class that should contain all general
    functionality for manipulation with hdf5 files.

    It only stores filename as ``self.h5_filename``, then opens and stores
    a handle to hdf5 file as ``self.h5_f``.
    """

    def __init__(self, h5_filename):
        """
        Args:
            h5_filename (str): path to hdf5 file with results
        """

        self.h5_filename = h5_filename
        logger.debug('self.h5_filename: %s', self.h5_filename)

        self.h5_f = h5py.File(self.h5_filename, 'r+')


    def get_list_of_groups_as_dict(self, starts_with):
        """
        Args:
            starts_with (str): groups prefix

        Returns:
            dict -- key is int of group number, value is group name

        """
        return {int(x.split('_')[1]): x for x in self.h5_f.keys() if x.startswith(starts_with)}
