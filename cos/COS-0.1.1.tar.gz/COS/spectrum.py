""" Methods for spectra extracted from the CalCOS pipeline

"""

from __future__ import division, print_function

from astropy.table import Table, Column
from astropy.units import angstrom, erg, s, cm

from scipy.interpolate import interp1d
from scipy.ndimage import uniform_filter1d as smooth

import numpy as np


class COSx1dSpectrum(object):
    """ Class representation of an x1d spectrum extracted using the COS
    pipeline CalCOS.

    Parameters
    ----------
    wavelength : array, shape (N,)
        The wavelength array for the spectrum (Angstrom).

    flux : ndarray, shape (N,)
        The flux density (erg / cm^2 / s / Angstrom).

    error : ndarray, shape (N,)
        Error on the flux.

    data_quality : ndarray, shape (N,)
        Data quality flags.

    gross : ndarray, shape (N,)
        Gross count rate.

    background : ndarray, shape (N,)
        Background count rate.

    net : ndarray, shape (N,)
        Net count rate, (gross - background) / eps, where eps is the
        flat fielding.

    header : dict
        FITS primary HDU header keyword values.

    meta : dict
        FITS table HDU header keyword values.

    """

    def __init__(self, wavelength, flux, error, data_quality, gross,
                 background, net, header, meta):

        if wavelength.ndim != 1 or wavelength.shape != flux.shape:
            raise ValueError('wavelength and flux need to be one-dimensional '
                             'arrays with the same shape')

        flags = dict(data_quality=data_quality,
                     weights=np.ones_like(wavelength))

        self.wavelength = wavelength * angstrom
        self.flux = flux * erg / cm ** 2 / s / angstrom
        self.error = error * erg / cm ** 2 / s / angstrom
        self.gross = gross / s
        self.background = background / s
        self.net = net / s
        self.flags = flags
        self.header = header
        self.meta = meta
        self.exptime = np.ones_like(wavelength) * self.meta['EXPTIME'] * s
        self.mask = np.zeros_like(self.wavelength, dtype=bool)

    def smooth_background(self, smoothing_length, check=False):
        """ Performs 1D boxcar background smoothing, after masking the Lya
        and OI geocoronal emission lines.

        Parameters
        ----------
        smoothing_length : int
            Background smoothing length (pixels).

        check : bool
            Option to plot a comparison between the smoothed and unsmoothed
            background and provide an option to change the smoothing length.

        Notes
        -----
        The background level is interpolated across geocoronal lines and set
        to zero in regions of bad data quality.

        """

        OI = (self.wavelength.value > 1300) & (self.wavelength.value < 1307.5)
        Lya = (self.wavelength.value > 1213) & (self.wavelength.value < 1218)
        mask = OI | Lya | self.mask

        decision = 'n'

        while decision != 'y':

            smoothed_background = np.zeros_like(self.background.value)
            smoothed_background[~mask] = smooth(
                self.background.value[~mask], smoothing_length)

            if len(smoothed_background[~mask]) != 0:
                smoothed_background = np.interp(
                    self.wavelength, self.wavelength[~mask],
                    smoothed_background[~mask])
                smoothed_background[self.mask] = 0.0

            else:
                smoothed_background[:] = 0.0

            if check:

                print('Plotting background...')
                import matplotlib.pyplot as pl

                pl.plot(self.wavelength.value, self.background.value, color='k',
                        label='unsmoothed')
                pl.plot(self.wavelength.value, smoothed_background, color='r',
                        label='smoothed')

                pl.legend(fancybox=True)
                pl.xlabel('Wavelength ($\\AA$)')
                pl.ylabel('Background (count s$^{-1}$)')

                pl.show()

                decision = raw_input('Adopt this backgound? y/n : ')

                if decision == 'y':
                    self.background = smoothed_background / s

                else:
                    smoothing_length = int(raw_input(
                        'Enter new smoothing length : '))

            else:

                decision = 'y'
                self.background = smoothed_background / s

    def interpolate(self, wavelength, kind='nearest', bounds_error=False,
                    fill_value=0):
        """ Interpolates onto a new wavelength grid and returns a new
        `COS.spectrum.COSx1dSpectrum` instance.

        Parameters
        ----------
        wavelength : array, shape (N,)
            The wavelength array on which to interpolate the flux.

        kind : str or int, optional (default = `nearest`)
            Specifies the kind of interpolation as a string (`linear`,
            `nearest`, `zero`, `slinear`, `quadratic`, `cubic` where
            `slinear`, `quadratic` and `cubic` refer to a spline
            interpolation of first, second or third order) or as an integer
            specifying the order of the spline interpolator to use.

        bounds_error : bool, optional (default = False)
            If True, an error is thrown any time interpolation is attempted
            on a wavelength point outside of the range of the original
            wavelength map (where extrapolation is necessary). If False,
            out of bounds values are assigned `fill_value`. By default,
            an error is raised.

        fill_value : float, optional (default = 0)
            If provided, then this value will be used to fill in for
            requested wavelength points outside of the original wavelength
            map.

        Notes
        -----
        Use of this method causes data quality flags to be set to 0. A new
        class instance is returned to ensure a copy of the original spectrum
        is retained with the data quality flags intact.

        """

        flux = interp1d(
            self.wavelength, self.flux, kind=kind, bounds_error=bounds_error,
            fill_value=fill_value)(wavelength)

        error = interp1d(
            self.wavelength, self.error, kind=kind, bounds_error=bounds_error,
            fill_value=fill_value)(wavelength)

        gross = interp1d(
            self.wavelength, self.gross, kind=kind, bounds_error=bounds_error,
            fill_value=fill_value)(wavelength)

        background = interp1d(
            self.wavelength, self.background, kind=kind,
            bounds_error=bounds_error, fill_value=fill_value)(wavelength)

        net = interp1d(
            self.wavelength, self.net, kind=kind, bounds_error=bounds_error,
            fill_value=fill_value)(wavelength)

        data_quality = np.zeros_like(wavelength)

        return self.__class__(wavelength, flux, error, data_quality,
                              gross, background, net, self.header, self.meta)

    def write(self, filename, overwrite=False):

        """ Write the spectrum to a file.

        filename : str
            Spectrum filename.

        overwrite : bool, optional
            Option to overwrite (default = True).

        """

        wavelength = Column(self.wavelength, name='WAVELENGTH')
        flux = Column(self.flux, name='FLUX')
        error = Column(self.error, name='ERROR')
        gross = Column(self.gross, name='GROSS')
        background = Column(self.background, name='BACKGROUND')
        net = Column(self.net, name='NET')
        dq = Column(self.flags['data_quality'], name='DQ')

        t = Table([wavelength, flux, error, gross, background, net, dq],
                  meta=self.meta)

        t.write(filename, overwrite=overwrite)