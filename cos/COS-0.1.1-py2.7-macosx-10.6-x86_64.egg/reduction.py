""" For reducing raw COS data using the CalCOS pipeline.

"""

from __future__ import division, print_function

from astropy.units import deg, s, angstrom
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.io import fits

from glob import glob

import numpy as np

import sys
import os


class RawData(object):
    """
    Describes an uncalibrated COS data set downloaded from the MAST archive.
    Includes methods for data reduction using the CalCOS pipeline.

    Parameters
    ----------
    data_path : str, optional
        Path to the  raw data products (defaults to the working directory).

    calibration_path : str, optional
        Path to the calibration products (defaults to the working directory).

    Attributes
    ----------
    path : str
        Location of the raw data products.

    asn : list
        CalCOS input files.

    targets : str or tuple of str
        Target name(s).

    coordinates : `astropy.coordinates.SkyCoord`
        Target coordinates.

    info : `astropy.table.Table`
        Tabulated information on the data set, with the following column names:
            `TARGNAME` : Target name.
            `ROOTNAME` : Rootname for data files.
            `DETECTOR` : Detector name, e.g. `FUVA`
            `GRATING` : Grating.
            `CENWAVE` : Central wavelength setting.
            `FP-POS` : FP-POS.
            `EXPTIME` : Exposure time.

    """

    def __init__(self, data_path='./', calibration_path='./'):

        self.path = os.path.abspath(data_path)
        self.asn = glob('{0}/*asn*'.format(self.path))

        if len(self.asn) == 0:
            raise AssertionError(
                'No raw data products in the specified directory!')

        os.environ['lref'] = calibration_path

        asn_headers = [fits.getheader(item) for item in self.asn]
        names = np.unique([header['TARGNAME'] for header in asn_headers])
        ra = np.unique([header['RA_TARG'] for header in asn_headers])
        dec = np.unique([header['DEC_TARG'] for header in asn_headers])

        if len(names) > 1:
            print('INFO: Directory contains raw data for more than one target')

        self.targets = tuple(names) if len(names) > 1 else names[0]
        self.coordinates = SkyCoord(ra * deg, dec * deg)

        rawtag = glob('{0}/*rawtag*'.format(data_path))
        rawtag_headers = [fits.getheader(item) for item in rawtag]

        self.extraction = np.unique(
            ['{0}/{1}'.format(calibration_path,
             header['XTRACTAB'].split('$')[1]) for header in rawtag_headers])

        targname = [header['TARGNAME'] for header in rawtag_headers]
        rootname = [header['ROOTNAME'] for header in rawtag_headers]
        detector = [header['SEGMENT'] for header in rawtag_headers]
        grating = [header['OPT_ELEM'] for header in rawtag_headers]
        cenwave = [header['CENWAVE'] for header in rawtag_headers]
        fppos = [header['FPPOS'] for header in rawtag_headers]
        exptime = [fits.getdata(item, 2)[0]['STOP'] for item in rawtag]

        self.info = Table(
            [targname, rootname, detector, grating, cenwave, fppos, exptime],
            names=['TARGNAME', 'ROOTNAME', 'DETECTOR', 'GRATING', 'CENWAVE',
                   'FP-POS', 'EXPTIME'])
        self.info['CENWAVE'].unit = angstrom
        self.info['EXPTIME'].unit = s

    def write_summary_table(self, filename, **kwargs):
        """
        Writes information about the data set to a file.

        Parameters
        ----------
        filename : str
            Path and filename for the table.

        """

        self.info.write(filename, **kwargs)

    def set_extraction_windows(self, G130M, G160M, G140L, NUV):
        """
        Adjust extraction windows.

        Parameters
        ----------
        G130M : tuple of int
            Object and background window extraction sizes (in pixels) for
            the G130M grating.

        G160M : tuple of int
            Object and background window extraction sizes (in pixels) for
            the G160M grating.

        G140L : tuple of int
            Object and background window extraction sizes (in pixels) for
            the G140L grating.

        NUV : tuple of int
            Object and background window extraction sizes (in pixels) for
            the G230L grating.

        """

        for fh in self.extraction:

            hdulist = fits.open(fh, mode='update')
            table = hdulist[1].data

            g130m = ((table['OPT_ELEM'] == 'G130M') &
                     (table['APERTURE'] == 'PSA'))
            g160m = ((table['OPT_ELEM'] == 'G160M') &
                     (table['APERTURE'] == 'PSA'))
            g140l = ((table['OPT_ELEM'] == 'G140L') &
                     (table['APERTURE'] == 'PSA'))
            nuv = ((table['OPT_ELEM'] == 'G230L') &
                   (table['APERTURE'] == 'PSA'))

            table['HEIGHT'][g130m] = G130M[0]
            table['BHEIGHT'][g130m] = G130M[1]
            table['HEIGHT'][g160m] = G160M[0]
            table['BHEIGHT'][g160m] = G160M[1]
            table['HEIGHT'][g140l] = G140L[0]
            table['BHEIGHT'][g140l] = G140L[1]
            table['HEIGHT'][nuv] = NUV[0]
            table['BHEIGHT'][nuv] = NUV[1]

            hdulist.flush()
            hdulist.close()

    def set_background_smoothing(self, background_smoothing_length):
        """
        Sets the smoothing length for 2D boxcar smoothing in CalCOS.

        Parameters
        ----------
        background_smoothing_length : int, optional
            Set to a small value if background smoothing later in 1D is
            desired.

        """

        for fh in self.extraction:

            hdulist = fits.open(fh, mode='update')
            table = hdulist[1].data

            table['BWIDTH'][table['APERTURE'] == 'PSA'] = \
                background_smoothing_length

            hdulist.flush()
            hdulist.close()

    def reduce(self, output_directory):
        """
        Runs the CalCOS pipeline.

        Parameters
        ----------
        output_directory : str
            Path for the reduced data products.

        """

        try:
            import calcos

        except:
            raise ImportError('CalCOS not installed')

        print('\nWill run CalCOS on the following raw data products:\n')
        self.info.pprint(max_lines=50)
        run = raw_input('\nContinue? (y)/n  ')

        if run != 'n':
            for asn in self.asn:
                calcos.calcos(asn, verbosity=2, outdir=output_directory)


def main(args=None):
    """ This is the main function called by the `runcalcos` script.

    """

    from astropy.utils.compat import argparse
    from astropy.extern.configobj import configobj, validate

    from pkg_resources import resource_stream

    parser = argparse.ArgumentParser(
        description='Run the COS pipeline CalCOS using the data and '
                    'parameters in a configuration file to be specified. To '
                    'dump a default configuration file: runcalcos -d')

    parser.add_argument('config', help='path to the configuration file')

    config = resource_stream(__name__, '/config/runcalcos.cfg')
    spec = resource_stream(__name__, '/config/runcalcos_specification.cfg')

    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            cfg = configobj.ConfigObj(config)
            cfg.filename = '{0}/runcalcos.cfg'.format(os.getcwd())
            cfg.write()
            return

    args = parser.parse_args(args)

    try:
        cfg = configobj.ConfigObj(args.config, configspec=spec)
        validator = validate.Validator()
        cfg.validate(validator)

    except:
        print(usage)
        raise IOError('Configuration file could not be read')

    data = RawData(**cfg['DATA'])

    g130m = (cfg['EXTRACTION'].pop('G130M_height'),
             cfg['EXTRACTION'].pop('G130M_background_height'))
    g160m = (cfg['EXTRACTION'].pop('G160M_height'),
             cfg['EXTRACTION'].pop('G160M_background_height'))
    g140l = (cfg['EXTRACTION'].pop('G140L_height'),
             cfg['EXTRACTION'].pop('G140L_background_height'))
    nuv = (cfg['EXTRACTION'].pop('NUV_height'),
           cfg['EXTRACTION'].pop('NUV_background_height'))

    data.set_extraction_windows(g130m, g160m, g140l, nuv)
    data.set_background_smoothing(**cfg['EXTRACTION'])

    data.reduce(**cfg['REDUCTION'])
