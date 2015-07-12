import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np


def linspacestep(start, stop, step=1):
    # Find an integer number of steps
    numsteps = _np.int((stop-start)/step)

    # Do a linspace over the new range
    # that has the correct endpoint
    return _np.linspace(start, start+step*numsteps, numsteps+1)
