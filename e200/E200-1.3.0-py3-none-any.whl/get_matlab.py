import glob
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as np
import platform
import logging
logger = logging.getLogger(__name__)

__all__ = ['get_matlab', 'is_facet_srv']


def get_matlab(display=False, splash=False):
    system = platform.system()

    if is_facet_srv():
        matlab_base = 'fmatlab'
    elif system == 'Darwin':
        matlabs = glob.glob('/Applications/MATLAB_R*/bin/matlab')
        if np.size(matlabs) > 1:
            logger.warning('Multiple matlabs found!')
        matlab_base = matlabs[0]
    elif system == 'Linux':
        home = _os.environ['HOME']
        matlab_base = _os.path.join(home, 'Matlab/bin/./matlab')
       
    options = ''
    if not display:
        options = options + ' -nodisplay'

    if not splash:
        options = options + ' -nosplash'

    return matlab_base + options


def is_facet_srv():
    nodename = platform.node()
    if nodename[0:-2] == 'facet-srv':
        return True
    else:
        return False
