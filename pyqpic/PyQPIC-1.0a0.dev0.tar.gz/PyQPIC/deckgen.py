#!/usr/bin/env python3

# ========================
# QuickPIC Deck Generator
# ========================
import numpy as _np
import jinja2 as jj
from . import classes as _cl


def deckgen(
        plasma, bunches, box, magic, qpic, filename=None, fid=None, verbose=True
        ):
    beampos = _cl.BeamPositioning()
    phas_samp = _cl.PhaseSpaceSampling()
    # =====================================
    # Generate jinja template object
    # =====================================
    loader            = jj.PackageLoader('PyQPIC', 'resources/templates')
    env               = jj.Environment(loader=loader, trim_blocks=True)
    template          = env.get_template('rpinput')
    
    # =====================================
    # Create output file for writing
    # =====================================
    if (fid is None and filename is None) or (fid is not None and filename is not None):
        raise ValueError('Must use either fid or filename')
    if filename is not None:
        fid = open(filename, 'w+')
    
    # =====================================
    # Use jinja template object to create
    # a stream with substitutions in it
    # =====================================
    stream = template.stream(
        qpic              = qpic,
        magic             = magic,
        bunches           = bunches,
        plasma            = plasma,
        box               = box,
        beampos           = beampos,
        phas_samp         = phas_samp,
        verbose           = verbose,
        nbeam             = _np.size(bunches)
        )
    # =====================================
    # Write stream contents to file
    # =====================================
    stream.disable_buffering()
    stream.dump(fid)

    # myfid = open('mytemp', 'w+')
    # stream.dump(myfid)
    # myfid.close()
    
    if filename is not None:
        fid.close()
    else:
        return fid
