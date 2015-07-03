from .E200_load_data import E200_load_data
from .get_remoteprefix import get_remoteprefix
import PyQt4.QtGui as QtGui
import glob
import os
import scisalt as pt
import re
import logging
logger = logging.getLogger(__name__)


def E200_load_data_gui(experiment=None, verbose=False):
    if experiment is not None:
        recent = 'nas/nas-li20-pm00/{}'.format(experiment)
    else:
        recent = 'nas/nas-li20-pm00/E*'

    # ======================================
    # Get most recent folder
    # ======================================
    pref = get_remoteprefix()
    temppath = os.path.join(pref, recent)
    temppath = max(glob.glob(os.path.join(temppath, '*')), key=os.path.getmtime)
    temppath = max(glob.glob(os.path.join(temppath, '*')), key=os.path.getmtime)
    temppath = max(glob.glob(os.path.join(temppath, '*')), key=os.path.getmtime)

    # ======================================
    # User selects file
    # ======================================
    app = pt.qt.get_app()  # NOQA
    loadfile = QtGui.QFileDialog.getOpenFileName(directory=temppath, filter='*.mat')
    if loadfile == '':
        input('No file chosen, press enter to close...')
        return
    loadfile  = loadfile[1:]
    p         = re.compile('nas/nas.*')
    loadmatch = p.search(loadfile)
    loadfile  = loadmatch.group()
    # loadfile  = 'nas/nas-li20-pm00/E217/2015/20150504/E217_16808/E217_16808.mat'

    logstring = 'File to load is: {}'.format(loadfile)
    if verbose:
        print('In order to load file:\ndata = E200.E200_load_data(\'{}\')'.format(loadfile))

    logger.info(logstring)

    return E200_load_data(loadfile)
