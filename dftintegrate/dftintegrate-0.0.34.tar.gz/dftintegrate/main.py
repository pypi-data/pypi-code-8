#!/usr/bin/env python3

import argparse
import os.path

from dftintegrate import msg
from dftintegrate.fourierfit import vaspdata, readdata, fitdata


def examples():
    """Prints the example for the help script."""

    script = "dftintegrate"
    explain = ("Create a Fourier fit of DFT data.")
    contents = [(("Fit VASP data with Fourier Series."),
                 ("dftintegrate -vasp -fit"),
                 ("Note this will simply produce some json data files, namely"
                  " data.json and fit.json. Some intermediate files will also"
                  " be created for the programs sake namely kmax.dat, "
                  "kpts_eigenvals.dat, and symops_trans.dat.")),

                (("Another feature."),
                 ("dftintegrate..."),
                 ("Notes.")),

                (("Another feature."),
                 ("dftintegrate..."),
                 ("Notes.")),

                (("More features to come."),
                 ("Another Example"),
                 ("A note."))]
    required = ("REQUIRED: VASP output data")
    output = ("RETURNS: Creates json data files of a fourier fit of the data.")
    details = ("See the README")
    outputfmt = (".json")

    msg.example(script, explain, contents, required,
                output, outputfmt, details)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-examples', help='See detail on how to use program.',
                        action='store_true')
    parser.add_argument('-vasp', help='As opposed to -qe for quatum espresso.'
                        ' data.', action='store_true')
    parser.add_argument('-qe', help='Using qe data as opposed to vasp.',
                        action='store_true')
    parser.add_argument('-fit', help='Generate the Fourier fit in fit.json.',
                        action='store_true')
    parser.add_argument('-read', help='Generate data.json', action='store_true')

    args = parser.parse_args()
    if args.examples:
        examples()
        exit(0)
    else:
        return args


def extract_vasp(path='./'):
    """
    Call vaspdata.py to extract vasp data and write kmax.dat,
    kpts_eigenvals.dat, and symops_trans.dat. Called in the path
    indicated, default is current directory.
    """
    bad = False
    kmax = True
    if not os.path.exists(path+'OUTCAR'):
        msg.err('OUTCAR does not exsist.')
        bad = True
    if not os.path.exists(path+'EIGENVAL'):
        msg.err('EIGENVAL does not exist.')
        bad = True
    if not os.path.exists(path+'KPOINTS'):
        msg.warn('KPOINTS does not exist, you\'ll need to make'
                 ' your own kmax.dat, see the README for more info.')
        kmax = False
    if bad:
        msg.info('The necessary VASP files are not in the specified directory.'
                 ' Note the default directory is your current working'
                 ' directory.')
        exit(0)
    else:
        vaspdata.VASPData(path, kmax=kmax)


def read_data(args, path='./'):
    """
    Call readdata.py to read kmax.dat, kpts_eigenvals.dat, and
    symops_trans.dat and creat data.json to be given to fitdata.py.
    Called in the path indicated, default is current directory.
    """
    bad = False
    if not os.path.exists(path+'kmax.dat'):
        msg.info('kmax.dat does not exist, creating one.')
        bad = True
    if not os.path.exists(path+'kpts_eigenvals.dat'):
        msg.info('kpts_eigenvals.dat does not exist, creating one.')
        bad = True
    if not os.path.exists(path+'symops_trans.dat'):
        msg.info('symops_trans.dat does not exist, creating one.')
        bad = True
    if bad:
        if args.vasp:
            extract_vasp()
        elif args.qe:
            msg.err('qe functionality not working in this version.')
            exit(0)
        else:
            msg.err('Please specify vasp or qe.')
            exit(0)
    readdata.ReadData(path)
    msg.info('data.json created.')


def get_fit(args, path='./'):
    """
    Call fitdata.py to generate a fit.json in the path indecated.
    Default path is the current directory.
    """
    if not os.path.exists(path+'data.json'):
        msg.info('data.json does not exist, creating one.')
        read_data(args)
    fitdata.FitData(path)
    msg.info('fit.json created.')


def main():
    print('here')
    args = _parse_args()
    if args.fit:
        get_fit(args)
    if args.read:
        read_data(args)
    elif not args.fit and not args.read:
        msg.err('Need more command line arguments. You must specify a DFT code'
                ' (-vasp or -qe) and an action i.e. -fit or -read.')
        exit(0)


if __name__ == '__main__':
    main()
