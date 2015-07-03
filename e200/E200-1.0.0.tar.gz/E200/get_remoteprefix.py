import ipdb  # NOQA
import os
import configparser as ConfigParser
import inspect
from PyQt4 import QtGui
import scisalt.qt as mtqt
import numpy as _np

__all__    = ['get_remoteprefix', 'set_remoteprefix', 'choose_remoteprefix', '_get_configpath', '_get_directory', '_get_datapath']
def_prefix = '/Volumes/PWFA_4big'


def choose_remoteprefix(pathstart=def_prefix, verbose=True):
    app = mtqt.get_app()  # NOQA
    if not os.path.isdir(pathstart):
        pathstart = '/'
    prefix = mtqt.getExistingDirectory(caption='Change prefix', directory=pathstart)
    if not os.path.isdir(prefix):
        raise IOError('No directory selected.')

    prefix = _test_prefix(prefix)

    if verbose:
        print('New prefix is: {}'.format(prefix))

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
    config = ConfigParser.ConfigParser()
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
    datapath = os.path.join(prefix, 'nas', 'nas-li20-pm00')
    return datapath


def _nas_in_path(prefix):
    datapath = _get_datapath(prefix)
    return os.path.isdir(datapath)


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
            prefix = choose_remoteprefix(verbose=False)
        elif clicked[2]:
            raise IOError('No valid directory chosen.')

    set_remoteprefix(prefix)
    return prefix


def set_remoteprefix(prefix, verbose=False):
    config = ConfigParser.ConfigParser()
    try:
        config.add_section('Prefs')
    except:
        pass

    config.set('Prefs', 'prefix', prefix)
    with open(_get_configpath(), 'wt') as configfile:
        config.write(configfile)
    if verbose:
        print('Remote prefix now: {}'.format(get_remoteprefix()))


def _get_configpath():
    this_path   = inspect.stack()[0][1]
    this_dir    = os.path.dirname(this_path)
    config_path = os.path.join(this_dir, 'FACET_data.cfg')

    return config_path


def _get_directory():
    window = QtGui.QFileDialog.getExistingDirectory(directory='/')
    return str(window)
