from __future__ import print_function
"""Utilities for converting MATCH SFH for use in TRILEGAL."""

import argparse
import numpy as np
import sys


def read_binned_sfh(filename):
    '''
    read the MATCH calcsfh, zcombine, or hybridMC output file as recarray.
    
    NOTE:
    This code calls genfromtext up to 3 times. There may be a better way to
    figure out how many background lines or if there is a header.
    It's a small file so it's not a big deal.
    '''
    dtype = [('lagei', '<f8'),
             ('lagef', '<f8'),
             ('dmod', '<f8'),
             ('sfr', '<f8'),
             ('sfr_errp', '<f8'),
             ('sfr_errm', '<f8'),
             ('mh', '<f8'),
             ('mh_errp', '<f8'),
             ('mh_errm', '<f8'),
             ('mh_disp', '<f8'),
             ('mh_disp_errp', '<f8'),
             ('mh_disp_errm', '<f8'),
             ('csfr', '<f8'),
             ('csfr_errp', '<f8'),
             ('csfr_errm', '<f8')]
    try:
        data = np.genfromtxt(filename, dtype=dtype)
    except ValueError:
        try:
            data = np.genfromtxt(filename, dtype=dtype, skip_header=6,
                                 skip_footer=1)
        except ValueError:
            data = np.genfromtxt(filename, dtype=dtype, skip_header=6,
                                 skip_footer=2)
    return data.view(np.recarray)


def process_match_sfh(sfhfile, outfile='processed_sfh.out', use_zdisp=False):
    '''
    Convert a match sfh file into a sfr-z table for trilegal

    Parameters
    ----------
    sfhfile : str
        MATCH sfh file

    outfile : str
        TRILEGAL sfr-z table filename to write to
    
    zdisp : bool
        Use z-dispersion reported by MATCH

    '''
    # trilegal line format (z-dispersion is a string so it can be empty if 0.)
    fmt = '{:.6g} {:.6g} {:.4g} {} \n'

    data = read_binned_sfh(sfhfile)
    sfr = data['sfr']
    # Trilegal only needs populated time bins, not fixed age array
    inds, = np.nonzero(sfr > 0)
    sfr = sfr[inds]
    to = data['lagei'][inds]
    tf = data['lagef'][inds]
    dlogz = data['mh'][inds]
    half_bin = np.diff(dlogz[0: 2])[0] / 2.
    if use_zdisp:
        zdisp = data['mh_disp'][inds]
    else:
        zdisp = [''] * len(to) 

    with open(outfile, 'w') as out:
        for i in range(len(to)):
            sfr[i] *= 1e3  # sfr is normalized in trilegal
            
            # MATCH conversion
            z1 = 0.02 * 10 ** (dlogz[i] - half_bin)
            z2 = 0.02 * 10 ** (dlogz[i] + half_bin)
            
            age1a = 1.0 * 10 ** to[i]
            age1p = 1.0 * 10 ** (to[i] + 0.0001)
            age2a = 1.0 * 10 ** tf[i]
            age2p = 1.0 * 10 ** (tf[i] + 0.0001)

            out.write(fmt.format(age1a, 0.0, z1, zdisp[i]))
            out.write(fmt.format(age1p, sfr[i], z1, zdisp[i]))
            out.write(fmt.format(age2a, sfr[i], z2, zdisp[i]))
            out.write(fmt.format(age2p, 0.0, z2, zdisp[i]))
            out.write(fmt.format(age1a, 0.0, z2, zdisp[i]))
            out.write(fmt.format(age1p, sfr[i], z2, zdisp[i]))
            out.write(fmt.format(age2a, sfr[i], z1, zdisp[i]))
            out.write(fmt.format(age2p, 0.0, z1, zdisp[i]))

    print('wrote {}'.format(outfile))
    return outfile