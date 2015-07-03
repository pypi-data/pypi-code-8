import platform
import numpy as np
import glob
import logging
logger = logging.getLogger(__name__)

__all__ = ['get_matlab', 'is_facet_srv']


def get_matlab(display=False, splash=False):
    if is_facet_srv():
        matlab_base = 'fmatlab'
    else:
        matlabs = glob.glob('/Applications/MATLAB_R*/bin/matlab')
        if np.size(matlabs) > 1:
            logger.warning('Multiple matlabs found!')
        matlab_base = matlabs[0]
       
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
