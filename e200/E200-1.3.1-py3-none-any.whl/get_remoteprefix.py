import sys as _sys
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    from PyQt4 import QtGui
    import scisalt.qt as mtqt

import configparser as _ConfigParser
import inspect as _inspect
import logging as _logging
import subprocess as _subprocess
import shlex as _shlex
from .get_matlab import get_matlab

logger = _logging.getLogger(__name__)

__all__    = ['get_remoteprefix', 'set_remoteprefix', 'choose_remoteprefix', '_get_configpath', '_get_directory', '_get_datapath']
def_prefix = '/Volumes/PWFA_4big'


def choose_remoteprefix(pathstart=def_prefix):
    app = mtqt.get_app()  # NOQA
    if not _os.path.isdir(pathstart):
        pathstart = _os.environ.get('HOME', _os.path.abspath(_os.sep))
    prefix = mtqt.getExistingDirectory(caption='Change prefix', directory=pathstart)
    if not _os.path.isdir(prefix):
        logger.critical('No directory selected: terminating.')
        raise IOError('No directory selected.')

    prefix = _test_prefix(prefix)
    set_remoteprefix(prefix)

    return prefix


def get_remoteprefix():
    app = mtqt.get_app()  # NOQA

    # =====================================
    # Default prefix
    # =====================================

    config_path = _get_configpath()

    # =====================================
    # Try to read the prefix
    # =====================================
    config = _ConfigParser.ConfigParser()
    try:
        config.read(config_path)
        prefix = config.get('Prefs', 'prefix')
    except:
        prefix = def_prefix
        set_remoteprefix(prefix)

    # =====================================
    # Test the prefix
    # =====================================
    prefix = _test_prefix(prefix)

    return prefix


def _get_datapath(prefix=None):
    if prefix is None:
        prefix = get_remoteprefix()
    datapath = _os.path.join(prefix, 'nas', 'nas-li20-pm00')
    return datapath


def _nas_in_path(prefix):
    datapath = _get_datapath(prefix)
    return _os.path.isdir(datapath)


def _test_prefix(prefix):
    while ( not _nas_in_path(prefix) ):
        title = 'Data location not found!'
        maintext = 'WARNING: Path to data doesn\'t exist!'
        infotext = 'Data not found at {}. Drive may not be mounted.'.format(prefix)
        buttons = _np.array([
            mtqt.Button('Try again.', QtGui.QMessageBox.AcceptRole, default=True),
            mtqt.Button('Locate folder containing /nas.', QtGui.QMessageBox.AcceptRole),
            mtqt.Button(QtGui.QMessageBox.Abort, escape=True),
            ])

        buttonbox = mtqt.ButtonMsg(title=title, maintext=maintext, infotext=infotext, buttons=buttons)
        clicked = buttonbox.clickedArray
        # Locate folder...
        if clicked[1]:
            prefix = choose_remoteprefix()
        elif clicked[2]:
            logger.critical('No valid directory chosen: terminating.')
            raise IOError('No valid directory chosen.')

    return prefix


def set_remoteprefix(prefix):
    config = _ConfigParser.ConfigParser()
    try:
        config.add_section('Prefs')
    except:
        pass

    config.set('Prefs', 'prefix', prefix)
    with open(_get_configpath(), 'wt') as configfile:
        config.write(configfile)

    matlab = get_matlab()
    command = '{matlab} -r "setpref(\'FACET_data\',\'prefix\',\'{prefix}\');exit;"'.format(matlab=matlab, prefix=prefix)

    logger.info('Setting remote prefix in Matlab: {}'.format(prefix))

    fnull = open(_os.devnull, 'w')
    _subprocess.call(_shlex.split(command), stdout=fnull, stderr=_subprocess.STDOUT)

    logger.info('Remote prefix now: {}'.format(prefix))


def _get_configpath():
    this_path   = _inspect.stack()[0][1]
    this_dir    = _os.path.dirname(this_path)
    config_path = _os.path.join(this_dir, 'FACET_data.cfg')

    return config_path


def _get_directory():
    window = QtGui.QFileDialog.getExistingDirectory(directory='/')
    return str(window)
