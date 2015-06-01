# -*- coding: utf-8 -*-

import os
import logging

_log = logging.getLogger(__name__)

_voicecom_path = os.path.expanduser('~/.voicecom')


def expand_path(*args):
    """Expands the '~/.voicecom' path using the given names.

    Requesting a path will create necessary directories on the fly.
    The last element will not be automatically created as a directory.
    """
    # Prepend the voicecom path.
    args = (_voicecom_path,) + args

    # Build the path and check for directories.
    path = ''
    for expansion in args[:-1]:
        path = os.path.join(path, expansion)
        # Create directory if necessary and desired.
        if not os.path.isdir(path):
            _log.debug('Creating directory at {}.'.format(path))
            os.mkdir(path)

    # Join the last element (usually the filename).
    return os.path.join(path, args[-1])
