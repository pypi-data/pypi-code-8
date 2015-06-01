""" Tools for reading 1D spectra extracted from the CalCOS pipeline,
for use in co-addition, and for reading and writing the line spread functions.

"""

from __future__ import division

from .spectrum import COSx1dSpectrum

from collections import OrderedDict

from astropy.units import angstrom, km, s, Quantity
from astropy.constants import c
from astropy.io import fits, ascii
from astropy.table import Table

from scipy.interpolate import interp1d

import numpy as np

import os

__all__ = ['read_x1d', 'read_lsf', 'limiting_equivalent_width',
           'significance_level']

datapath = os.path.split(os.path.abspath(__file__))[0] + '/'

dw_orig = dict(G130M=0.00997, G160M=0.01223, G140L=0.083, NUV=0.390)

c_kms = c.to(km / s)

# Cache for the LSF values
cache_lsf = {}


def read_x1d(filename):
    """ Reads an x1d format spectrum from CalCOS.

    Parameters
    ----------
    filename : str
        x1d filename.

    Returns
    -------
    x1dspec : dict
        Dictionary of `COS.spectrum.COS1DSpectrum` objects with keys
        corresponding to the detector segments (e.g. `FUVA`, `FUVB`).

    """

    hdulist = fits.open(filename)
    data = hdulist[1].data

    header, meta = OrderedDict(), OrderedDict()

    for key, val in hdulist[0].header.iteritems():
        if key != '':
            header[key] = val

    for key, val in hdulist[1].header.iteritems():
        if key != '':
            meta[key] = val

    x1dspec = dict()

    for i, segment in enumerate(data['SEGMENT']):

        this_header = header.copy()
        this_header['SEGMENT'] = segment

        x1dspec[segment] = COSx1dSpectrum(
            data[i]['WAVELENGTH'], data[i]['FLUX'], data[i]['ERROR'],
            data[i]['DQ'], data[i]['GROSS'], data[i]['BACKGROUND'],
            data[i]['NET'], this_header, meta)

    return x1dspec


def cross_correlate(s1, s2, ishift=0, width=15, s1_start=None, s1_end=None):
    """
    Normalised mean and covariance cross correlation offset between
    two input vectors of the same length.

    Parameters
    ----------
    s1 : array, shape (N,)
        Reference spectrum.

    s2 : array, shape (N,)
        Comparison spectrum.

    ishift : float, optional
        Approximate offset in pixels (default = 0).

    width : float, optional
        Search width in pixels (default = 15).

    s1_start, s1_end : float, optional
        Start and end index for region in s1 containing features.

    Returns
    -------
    offset : array, shape(N,)
        Offset of s2 from s1 in pixels.

    corr : array, shape(N,)
        Output correlation.

    """

    approx = np.round(ishift)  # Nearest integer
    ns = len(s1)

    if s1_start is None:
        s1_start = 0  # s1 start index

    if s1_end is None:
        s1_end = ns - 1  # s1 end index

    # Get start and end index for s2 template:
    s2_start = ((s1_start - approx + width / 2)
                if (s1_start - approx + width / 2) > 0 else 0)
    s2_end = ((s1_end - approx - width / 2)
              if (s1_end - approx - width / 2) < (ns - 1) else (ns - 1))

    # Check the length of the template:
    nt = s2_end - s2_start + 1
    if nt < 1.0:
        raise ValueError('cross correlation region too small, '
                         'or width/ishift too large')

    template2 = s2[s2_start:(s2_end + 1)]  # template for s2
    corr = np.zeros(width)  # correlation matrix

    # Get statistics on s2 template:
    mean2 = np.mean(template2)
    std2 = np.std(template2)
    diff2 = template2 - mean2

    # Cross correlate:
    for i in range(width):

        # Extract s1 template:
        s1_start = s2_start - width / 2 + approx + i
        s1_end = s1_start + nt - 1
        template1 = s1[s1_start:(s1_end + 1)]

        # Statistics on the template:
        mean1 = np.mean(template1)
        std1 = np.std(template1)
        diff1 = template1 - mean1

        # Check variance for zeros:
        if (std1 == 0) or (std2 == 0):
            raise ValueError('zero variance computed in cross correlation')

        # Compute the cross-correlation:
        corr[i] = np.sum(diff1 * diff2) / (std1 * std2)

    # Find index for the correlation maximum:
    k = np.argmax(corr)

    # Return zero offset if the correlation maximum is on the edge of the
    # search area (we have failed to find a correlation peak in this case):
    if (k == 0) or (k == (width - 1.0)):
        print('WARNING: correlation maximum on edge of search area, returning '
              'zero offset')
        offset = 0
        return offset, corr

    # Use quadratic refinement to pin down the offset:
    kmin = ((corr[k - 1] - corr[k]) /
            (corr[k - 1] + corr[k + 1] - 2.0 * corr[k]) - 0.5)
    offset = k + kmin - width / 2 + approx

    return offset, corr


def scale_factor(wavelength1, flux1, error1, wavelength2, flux2, error2):
    """ Find the multiplicative factor to rescale flux2, so its median will
    match flux1 where they overlap in wavelength.

    Parameters
    ----------
    wavelength1, wavelength2 : arrays, shape (N,), (M,)
        Dispersion for spectrum 1 and 2.

    flux1, flux2 : arrays, shape (N,), (M,)
       Flux for spectrum 1 and 2.

    error1, error2 : arrays, shape (N,), (M,)
        Flux error for spectrum 1 and 2.

    Returns
    -------
    scaling : float
        Scale factor.

    Notes
    -----
    Errors are used to identify bad pixels.

    """

    wmin = max(wavelength1.min(), wavelength2.min())
    wmax = min(wavelength1.max(), wavelength2.max())

    good1 = ((error1 > 0) & ~np.isnan(flux1) &
             (wmin < wavelength1) & (wavelength1 < wmax))
    good2 = ((error2 > 0) & ~np.isnan(flux2) &
             (wmin < wavelength2) & (wavelength2 < wmax))

    if good1.sum() < 3 or good2.sum() < 3:
        raise ValueError('Too few good pixels to use for scaling')

    median1 = np.median(flux1[good1])
    median2 = np.median(flux2[good2])

    if not (median1 > 0) or not (median2 > 0):
        print('Bad medians: ', str(median1), str(median2),
              ' returning unit scaling')
        scaling = 1
        return scaling

    scaling = median1 / median2

    return scaling


class LSF(object):
    """ Represents a COS line-spread function.

    Parameters
    ----------
    grating : {'G130M', 'G160M', 'G140L', 'NUV'}
        Grating name. All NUV gratings have the same LSF, and are denoted `NUV`.

    Attributes
    ----------
    lsf : `astropy.table.Table`
        The COS line-spread function as a function of pixel offset from the
        centre.

    dispersion : ndarray, shape (N,)
        Dispersion (Angstrom).

    pixel_width : float
        Pixel width (Angstrom).

    """

    def __init__(self, grating):

        self.lsf = ascii.read('{0}/LSF/{1}.txt'.format(datapath, grating))
        self.dispersion = self.lsf['relpix'] * dw_orig[grating]
        self.pixel_width = dw_orig[grating]

    def interpolate(self, dw):
        """ Interpolate LSF to a new pixel width.

        Parameters
        ----------
        dw : float
            The new pixel width (Angstrom).

        """

        t = np.arange(0, self.dispersion[-2], dw)
        new_disp = np.concatenate([-t[::-1][:-1], t])

        wavs = self.lsf.colnames[1:]
        new_lsf = []
        for w in wavs:
            new_lsf.append(
                interp1d(self.dispersion, self.lsf[w], kind='cubic')(new_disp))

        t = np.arange(len(new_disp) // 2 + 1)
        new_pix = np.concatenate([-t[::-1][:-1], t])
        lsf = Table([new_pix] + new_lsf, names=self.lsf.colnames)

        self.lsf = lsf
        self.dispersion = new_disp
        self.pixel_width = dw

    def write(self, wavelength, dw):
        """ Write a file giving the COS line spread function at a given
        wavelength for constant pixel width dw (both in Angstrom), suitable
        for input to VPFIT (http://www.ast.cam.ac.uk/rfc/vpfit.html).

        Parameters
        ----------
        wavelength : float
            Wavelength at which to compute the LSF (Angstrom).

        dw : float
            Pixel width (Angstrom).

        """

        outname = 'LSF/LSF_{0:.1f}.txt'.format(wavelength)

        if self.pixel_width != dw:
            self.interpolate(dw)

        if not os.path.lexists('./LSF'):
            os.mkdir('./LSF')

        wavs = [float(n[1:]) for n in self.lsf.colnames[1:]]
        lsf1 = np.array([self.lsf[n] for n in self.lsf.colnames[1:]])

        new_lsf = []
        for ipix in range(lsf1.shape[1]):
            new_lsf.append(np.interp(wavelength, wavs, lsf1[:, ipix]))

        lsf = Table([self.lsf['relpix'].tolist(), new_lsf])
        lsf.write(outname, format='ascii.fixed_width_no_header', delimiter='')


def read_lsf(grating, dw_new=None):
    """ Read the COS line spread function, optionally interpolated to
    a new pixel width.

    Parameters
    ----------
    grating : {`G130M`, `G160M`, `G140L`, `NUV`}
        Either 'NUV' for all near UV gratings, or the name of the far UV
        COS grating.

    dw_new : float
        The new pixel width in Angstroms.  Default is `None`, which
        returns the original LSF.

    Returns
    -------
    LSF : `COS.utils.LSF` instance
        The line spread function.

    """

    # See if we've already calculated it:
    try:
        return cache_lsf['{0}_{1}'.format(grating, dw_new)]

    except KeyError:
        pass

    lsf = LSF(grating)
    lsf.interpolate(dw_new)

    cache_lsf['{0}_{1}'.format(grating, dw_new)] = lsf

    return lsf


def limiting_equivalent_width(significance, wavelength, b, snpix,
                              dispersion=None, smoothing=1):
    """ Determines the limiting equivalent width for an absorption feature
    in either of the G130M or G160M gratings, taking into account the
    non-poissonian noise properties of the data, using Equations 4-5,
    7 and 9-10 of Keeney et al. (2012), PASP, 124, 918.

    Parameters
    ----------
    significance : int
        Significance level of limit (number of standard deviations).

    wavelength : float or array of floats, shape (N,)
        Observed wavelength of the line (Angstrom).

    b : float
        An estimate of the Doppler broadening parameter (km/s).

    snpix : float or array of floats, shape (N,)
        Signal-to-noise ratio per spectral pixel.

    dispersion : float, optional
        Dispersion in Angstrom/pixel (defaults to the G130M value for
        wavelengths <= 1425 A and the G160M value otherwise).

    smoothing : float, optional
        The number of pixels the spectrum has been re-binned by
        (default = 1 (no re-binning)).

    Returns
    -------
    lim_eqw : `astropy.units.Quantity`
        Limiting equivalent width (Angstrom).

    """

    if isinstance(wavelength, Quantity):
        wavelength = wavelength.to(angstrom)

    else:
        wavelength = wavelength * angstrom

    if isinstance(b, Quantity):
        b = b.to(km / s)

    else:
        b = b * km / s

    if isinstance(dispersion, Quantity):
        dispersion = dispersion.to(angstrom)

    elif dispersion is not None:
        dispersion = dispersion * angstrom

    elif isinstance(wavelength, (list, np.ndarray)):
        dispersion = np.empty_like(wavelength)
        dispersion[wavelength.value <= 1425] = 0.00997 * angstrom
        dispersion[wavelength.value > 1425] = 0.01223 * angstrom

    elif wavelength <= 1425:
        dispersion = 0.00997 * angstrom

    else:
        dispersion = 0.01223 * angstrom

    dx = b * wavelength / (c_kms * dispersion)
    xopt = 1.605 * dx + 5.1 * dx ** -0.25
    eta = 0.15 + xopt ** 0.37
    fcx = 0.743 - 0.185 * np.exp(-dx / 11.6)

    sn1 = snpix / (0.15 + smoothing ** 0.37) if smoothing != 1 else snpix

    lim_eqw = (significance * dispersion / sn1) * xopt / (eta * fcx)

    return lim_eqw


def significance_level(eqw, wavelength, b, snpix, dispersion=None, smoothing=1):
    """ Determines the significance level of a line using Equations 4,
    7 and 9-11 of Keeney et al. (2012), PASP, 124, 918.

    Parameters
    ----------
    eqw : float
        Observed equivalent width of the line (Angstrom).

    wavelength : float or array of floats, shape (N,)
        Observed wavelength (Angstrom).

    b : float
        Doppler broadening parameter (km/s).

    snpix : float or array of floats, shape (N,)
        Signal-to-noise ratio per spectral pixel.

    dispersion : float, optional
        Dispersion in Angstrom/pixel (defaults to the G130M value for
        wavelengths <= 1425 A and the G160M value otherwise).

    smoothing : float, optional
        The number of pixels the spectrum has been re-binned by
        (default = 1 (no re-binning)).

    Returns
    -------
    sig_level : float
        Significance level in number of standard deviations.

    """

    if isinstance(eqw, Quantity):
        eqw = eqw.to(angstrom)

    else:
        eqw = eqw * angstrom

    if isinstance(wavelength, Quantity):
        wavelength = wavelength.to(angstrom)

    else:
        wavelength = wavelength * angstrom

    if isinstance(b, Quantity):
        b = b.to(km / s)

    else:
        b = b * km / s

    if isinstance(dispersion, Quantity):
        dispersion = dispersion.to(angstrom)

    elif dispersion is not None:
        dispersion = dispersion * angstrom

    elif isinstance(wavelength, (list, np.ndarray)):
        dispersion = np.empty_like(wavelength)
        dispersion[wavelength <= 1425] = 0.00997
        dispersion[wavelength > 1425] = 0.01223

    elif wavelength <= 1425:
        dispersion = 0.00997 * angstrom

    else:
        dispersion = 0.01223 * angstrom

    dx = b * wavelength / (c_kms * dispersion)
    xopt = 1.605 * dx + 5.1 * dx ** -0.25
    eta = 0.15 + xopt ** 0.37
    fcx = 0.743 - 0.185 * np.exp(-dx / 11.6)

    sn1 = snpix / (0.15 + smoothing ** 0.37) if smoothing != 1 else snpix

    sig_level = sn1 * (eqw / dispersion) * eta * (fcx / xopt)

    return sig_level.value
