#!/usr/bin/env python3

import argparse
import os.path

from dftintegrate import msg
from dftintegrate.fourier import vaspdata, readdata, fitdata, integratedata


def examples():
    """Prints the example for the help script."""

    script = "dftintegrate"
    explain = ("Create a Fourier fit of DFT data.")
    contents = [(("Fit VASP data with Fourier Series."),
                 ("dftintegrate -vasp -fit"),
                 ("Note, this will simply produce some json data files, namely"
                  " data.json and fit.json. Some intermediate files will also"
                  " be created for the programs sake namely kmax.dat, "
                  "kpts_eigenvals.dat, and symops_trans.dat.")),

                (("Integrate VASP data with rectangles and "
                  "Gaussian Quadrature."),
                 ("dftintegrate -vasp -integrate"),
                 ("Note, this will produce integral.json.")),

                (("You only need to specify which DFT code was used if you"
                  " need to create a data.json. If the json files needed "
                  "already exsist and a DFT code was specified, the DFT "
                  "code specifier will be ignored."),
                 ("dftintegrate -fit"),
                 ("Case 1, assuming I have a data.json I can just say -fit and"
                  " it will use the data.json. The only files that are over"
                  " written are the ones that correspond to a flag. If fit "
                  "is specified, fit.json will be over written but data.json"
                  " will not be, if it exsists it is used.\nCase 2, assuming"
                  " there is no data.json an error will be raised saying I"
                  " need to specify a DFT code.\nCase 3, Look at Example 1,"
                  " if there is already a data.json the vasp flag is "
                  "ignored.")),

                (("More features to come."),
                 ("Another Example"),
                 ("A note."))]
    required = ("REQUIRED: VASP or Quantum Espresso output data")
    output = ("RETURNS: Creates json data files from the data. Also creates"
              " a few .dat text files for the programs sake, can be ignored")
    details = ("See the README for more detail.")
    outputfmt = (".dat, .json")

    msg.example(script, explain, contents, required,
                output, outputfmt, details)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-examples', help='See details on how to use program.',
                        action='store_true')
    parser.add_argument('-vasp', help='As opposed to -qe for quatum espresso.'
                        ' data.', action='store_true')
    parser.add_argument('-qe', help='Using qe data as opposed to vasp.',
                        action='store_true')
    parser.add_argument('-fit', help='Generate the Fourier fit in fit.json.',
                        action='store_true')
    parser.add_argument('-read', help='Generate data.json',
                        action='store_true')
    parser.add_argument('-integrate', help='Generate integral.json.',
                        action='store_true')
    parser.add_argument('-points', help='Number of integration points.')
    parser.add_argument('-quiet', help='Supress output',
                        action='store_true')

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
        msg.err('The necessary VASP files are not in the specified directory.'
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
        if not args.quiet:
            msg.info('kmax.dat does not exist, attempting to create.')
        bad = True
    if not os.path.exists(path+'kpts_eigenvals.dat'):
        if not args.quiet:
            msg.info('kpts_eigenvals.dat does not exist, attempting to create.')
        bad = True
    if not os.path.exists(path+'symops_trans.dat'):
        if not args.quiet:
            msg.info('symops_trans.dat does not exist, attempting to create.')
        bad = True
    if bad:
        if args.vasp:
            extract_vasp(path=path)
        elif args.qe:
            msg.err('qe functionality not working in this version, no '
                    'files created.')
            exit(0)
        else:
            msg.err('Please specify vasp or qe.')
            exit(0)
    readdata.ReadData(path)
    if not args.quiet:
        msg.info('data.json created.')


def get_fit(args, path='./'):
    """
    Call fitdata.py to generate a fit.json in the indicated
    directory. Default path is the current directory.
    """
    if os.path.exists(path+'data.json') and not args.read:
        if not args.quiet:
            msg.warn('You specified vasp/qe but there is already a data.json'
                     ', the vasp/qe flag will be ignored. If you\'d like to '
                     'make a new data.json you can force it with the read'
                     ' flag.')
    if not os.path.exists(path+'data.json'):
        if not args.quiet:
            msg.info('data.json does not exist, attempting to create.')
        read_data(args, path=path)
    fitdata.FitData(path)
    if not args.quiet:
        msg.info('fit.json created.')


def integrate(args, path='./'):
    """
    Call integrate.py to generate an integral.json in the indicated
    directory. Default path is the current directory.
    """
    if os.path.exists(path+'fit.json') and not args.read:
        if not args.quiet:
            msg.warn('You specified vasp/qe but there is already a fit.json'
                     ', the vasp/qe flag will be ignored. If you\'d like to '
                     'make sure that vasp/qe data is being used you can force'
                     ' it by using the read flag then the fit flag, or erase'
                     ' data.json and fit.json.')
    if not os.path.exists(path+'fit.json'):
        if not args.quiet:
            msg.info('fit.json does not exist, attempting to create.')
        get_fit(args, path=path)
    integratedata.IntegrateData(path, args.points)
    if not args.quiet:
        msg.info('integral.json created.')


def main():
    args = _parse_args()
    if args.read:
        read_data(args)
    if args.fit:
        get_fit(args)
    if args.integrate:
        if not args.points:
            msg.err('If -integrate was specified you also need to specify '
                    '-points for the number of integration points. Example '
                    '-points 10.')
            exit(0)
        integrate(args)
    elif not args.fit and not args.read and not args.integrate:
        msg.err('Need more command line arguments. You must specify a DFT code'
                ' (-vasp or -qe) and/or an action i.e. -integrate or -read.')
        exit(0)


if __name__ == '__main__':
    main()
