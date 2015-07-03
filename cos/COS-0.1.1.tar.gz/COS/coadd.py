""" Routines for co-adding x1d files from CalCOS. Currently only deals with
data from the G130M, G160M and G230L gratings.

"""

from __future__ import division, print_function

from .utils import read_x1d, scale_factor, cross_correlate

from astropy.convolution import Gaussian1DKernel, convolve
from astropy.units import angstrom, cm, s, erg
from astropy.table import Table, Column
from astropy.io import fits

from scipy.ndimage import uniform_filter1d as smooth

import matplotlib.pyplot as pl

import numpy as np

import glob
import os


def coadd_x1d(name, data_path, calibration_path, smooth_background=True,
              fuva_smooth=1000, fuvb_smooth=500, nuv_smooth=100,
              check_background=False, setup=3, nuv_shift=None, nuv_scale=None,
              correlation_offset=True, scale_spectra=True, plot=True,
              check_alignment=False, gehrels_error=True):
    """ Co-adds `x1d` spectra from CalCOS via a modified exposure time
    weighting scheme and writes to files.

    Parameters
    ----------
    name : str
        Name for the spectrum.

    data_path : str
        Directory containing x1d files for processing.

    calibration_path : str
        Directory containing calibration reference files.

    smooth_background : bool
        Set to False for no background smoothing
        (i.e. when adopting the default CalCOS background estimation).

    fuva_smooth : int, optional
        FUVA boxcar smoothing length (default = 1000 pixels).

    fuvb_smooth : int, optional
        FUVB boxcar smoothing length (default = 500 pixels).

    nuv_smooth : in, optional
        NUV boxcar smoothing length (default = 100 pixels).

    check_background : bool, optional
        Option to plot smoothed background (default = False).

    setup : float
        Specifies the instrument setup:
            setup = 1 G130M
            setup = 2 G160M
            setup = 3 both FUV M gratings (default)
            setup = 4 G230L
            setup = 5 both FUV M gratings plus G230L

    nuv_shift : array of floats, shape (N,)
        Array specifying G230L offsets in Angstroms (default = None).

    nuv_scale : array of floats, shape (N,)
        Array specifying G230L scale factors (default = None).

    correlation_offset : bool
        Option to perform cross-correlation analysis between FUV settings,
        shifting spectra to ensure they lie on the same wavelength solution
        (default = True).

    scale_spectra : bool
        Option to perform flux scaling between FUV settings, so their median
        flux values match in overlap regions (default = True).

    plot : bool
        Option to plot co-added spectra.

    check_alignment : bool
        Option to plot spectrum snapshots before and after co-alignment
        (default = False).

    gehrels_error : bool
        Option to adopt the Gehrels (1986) approximation for the upper
        confidence limit (default = True).

    Notes
    -----
    The background count rate is estimated independently of CalCOS by
    default. In such case it is therefore essential that CalCOS is run
    with background smoothing lengths set to a small value. If you want to
    keep the CalCOS background estimation, set smooth_background to False.

    """

    if nuv_shift is not None and not hasattr(nuv_shift, 'unit'):
        nuv_shift *= angstrom

    # Get x1d files:
    x1d_files = glob.glob('{0}/*x1d.fits'.format(data_path))
    print('Found {0} x1d files'.format(len(x1d_files)))

    # Read in x1d tables and headers:
    x1dspec = [read_x1d(fh) for fh in x1d_files]

    targname = x1dspec[0][x1dspec[0].keys()[0]].header['TARGNAME']
    pid = str(x1dspec[0][x1dspec[0].keys()[0]].header['PROPOSID'])

    fuv_spectra, nuv_spectra = [], []

    print('---------------------------------------------------------'
          '\nTARGNAME: {0}  PID: {1}'
          '\n---------------------------------------------------------'
          '\nvisit  detector  grating  cenwave  FP-POS  exposure time '
          '\n---------------------------------------------------------'
          '\n'.format(targname, pid))

    # Loop over x1d spectra:
    for i in range(len(x1dspec)):

        # Loop over detector segments:
        for j, detector in enumerate(x1dspec[i].keys()):

            # Ignore NUVC (affected by second order light):
            if detector == 'NUVC':
                continue

            spec = x1dspec[i][detector]
            spec.mask = spec.wavelength.value > 3350.0  # Exclude 2nd order
                                                        # light

            vnum = int(x1d_files[i].split('/')[-1][4:6])
            grating = spec.header['OPT_ELEM']
            cenwave = str(spec.header['CENWAVE'])

            # A and B stripes labelled opposite way round for NUV:
            if detector[:-1] == 'NUV':
                detector = 'NUVA' if detector == 'NUVB' else 'NUVB'

            fppos = spec.header['FPPOS']

            print('   {0}      {1}    {2}     {3}       {4}     {5}'.format(
                str(vnum), detector, grating, cenwave, str(fppos),
                str(spec.exptime[0])))

            ##############################################################
            # Some DQ values are ignored or de-weighted, and some are
            # thrown out all together. For the latter we set dq_wgt = 0.
            # The rest we set dq_wgt = 1. Pixels with DQ values flagged
            # for de-weighting (below) are de-weighted by halving the
            # exposure time. For NUV data we de-weight vignetted regions
            # (DQ=4)
            #
            #      1 = 2 ^ 0  = Reed-Solomon error       --> throw out
            #      4 = 2 ^ 2  = Detector shadow          --> throw out
            #      8 = 2 ^ 3  = Poorly calibrated region --> throw out
            #     16 = 2 ^ 4  = V low response region    --> throw out
            #     32 = 2 ^ 5  = Background feature       --> de-weight
            #     64 = 2 ^ 6  = Burst                    --> throw out
            #    128 = 2 ^ 7  = Pixel out of bounds      --> throw out
            #    256 = 2 ^ 8  = Fill data                --> throw out
            #    512 = 2 ^ 9  = PH out of bounds         --> throw out
            #   1024 = 2 ^ 10 = Low response region      --> throw out
            #   2048 = 2 ^ 11 = Bad time interval        --> throw out
            #   4096 = 2 ^ 12 = Low PHA feature          --> de-weight
            #   8192 = 2 ^ 13 = Gain-sag hole            --> de-weight
            #
            # More info on DQ flags at:
            # http://www.stsci.edu/hst/cos/pipeline/cos_dq_flags
            ##############################################################

            # Weighting scheme:
            if detector[:-1] == 'NUV':
                keep = ((spec.flags['data_quality'] == 0) |
                        (spec.flags['data_quality'] == 2 ** 2) |
                        (spec.flags['data_quality'] == 2 ** 5) |
                        (spec.flags['data_quality'] == 2 ** 12) |
                        (spec.flags['data_quality'] == 2 ** 13))
                de_weight = ((spec.flags['data_quality'] == 2 ** 2) |
                             (spec.flags['data_quality'] == 2 ** 5) |
                             (spec.flags['data_quality'] == 2 ** 12) |
                             (spec.flags['data_quality'] == 2 ** 13))

            else:
                keep = ((spec.flags['data_quality'] == 0) |
                        (spec.flags['data_quality'] == 2 ** 5) |
                        (spec.flags['data_quality'] == 2 ** 12) |
                        (spec.flags['data_quality'] == 2 ** 13))
                de_weight = ((spec.flags['data_quality'] == 2 ** 5) |
                             (spec.flags['data_quality'] == 2 ** 13) |
                             (spec.flags['data_quality'] == 2 ** 12))

            # Weight flags: 0 = discard pixel
            #               1 = keep pixel
            #               2 = de-weight pixel
            spec.flags['weights'] = np.zeros(len(spec.wavelength))
            spec.flags['weights'][keep], spec.flags['weights'][de_weight] = 1, 2

            # Mask bad flags:
            spec.mask = spec.mask | ~keep

            # Background smoothing option:
            if smooth_background:

                # NOTE: in smoothing the background we have to re-calculate
                # the net counts and error arrays...

                # Recover flatfielding (eps):
                eps = []
                for k in range(len(spec.gross)):
                    if spec.gross[k] != spec.background[k]:
                        eps.append(spec.net[k] /
                                   (spec.gross[k] - spec.background[k]))
                    else:
                        eps.append(1.0)
                eps = np.array(eps)

                # Smooth background count rate:
                if detector[:-1] == 'NUV':
                    spec.smooth_background(nuv_smooth, check_background)
                elif detector == 'FUVA':
                    spec.smooth_background(fuva_smooth, check_background)
                else:
                    spec.smooth_background(fuvb_smooth, check_background)

                # Get flatfield info:
                flatfile = spec.header['FLATFILE'][5:]
                fh = fits.open(calibration_path + flatfile)
                if detector in ['FUVA', 'FUVB']:
                    flat_hdr = fh[detector].header
                else:
                    flat_hdr = fh[1].header
                snr_ff = flat_hdr.get('snr_ff', 0.0)
                fh.close()

                # Get 1D spectrum extraction parameters:
                height = spec.meta['SP_HGT_' + detector[-1:]]
                bheight1 = spec.meta['B_HGT1_' + detector[-1:]]
                bheight2 = spec.meta['B_HGT2_' + detector[-1:]]

                # Recalculate net counts:
                spec.net = eps * (spec.gross - spec.background)

                # Calculate error terms:
                bgnorm = height / float(bheight1 + bheight2)
                if snr_ff > 0:
                    term1 = ((spec.net * spec.exptime /
                              float(height * snr_ff)) ** 2)
                else:
                    term1 = 0.0
                if detector[:-1] == 'NUV':
                    term2 = ((eps ** 2) * spec.exptime *
                             (spec.gross + spec.background *
                              (bgnorm / nuv_smooth)))
                elif detector == 'FUVA':
                    term2 = ((eps ** 2) * spec.exptime *
                             (spec.gross + spec.background *
                              (bgnorm / fuva_smooth)))
                elif detector == 'FUVB':
                    term2 = ((eps ** 2) * spec.exptime *
                             (spec.gross + spec.background *
                              (bgnorm / fuvb_smooth)))
                sum_terms = term1 + term2
                sum_terms = np.where(sum_terms > 0, sum_terms, 0.0)

                # Recalculate error:
                if gehrels_error:
                    # Gehrels (1986) approximation for upper confidence limit:
                    spec.error = (1 + np.sqrt(sum_terms + 0.75)) / spec.exptime
                else:
                    spec.error = np.sqrt(sum_terms) / spec.exptime

                # Get sensitivity curve:
                sens_file = spec.header['FLUXTAB'][5:]
                scidata = fits.open(calibration_path + sens_file)[1].data
                cond = ((scidata.CENWAVE == int(cenwave)) &
                        (scidata.OPT_ELEM == grating + '   ') &
                        (scidata.APERTURE == 'PSA ') &
                        (scidata.SEGMENT == detector))
                sens_wave = scidata.WAVELENGTH[cond][0]
                sens_curve = scidata.SENSITIVITY[cond][0]

                # Calibrate flux and error arrays:
                sens_curve = (np.interp(
                    spec.wavelength, sens_wave, sens_curve) *
                    angstrom * cm ** 2 / erg)
                spec.flux = spec.net / sens_curve
                spec.error /= sens_curve

                # Get TDS information:
                tds_file = spec.header['TDSTAB'][5:]
                tds = fits.open(calibration_path + tds_file)
                scidata = tds[1].data
                ref_time = tds[1].header['REF_TIME']
                nwl = scidata.NWL[j]
                nt = scidata.NT[j]
                tds_wa = scidata.WAVELENGTH[j]
                time = scidata.TIME[j]
                slope = scidata.SLOPE[j]          # 2D array
                intercept = scidata.INTERCEPT[j]  # 2D array
                maxt = len(time)
                maxwa = len(tds_wa)
                slope = np.reshape(slope, (maxt, maxwa))
                intercept = np.reshape(intercept, (maxt, maxwa))

                # Find the time interval that includes the time of observation:
                t_obs = ((spec.meta['EXPSTART'] + spec.meta['EXPEND']) / 2)
                if nt == 1 or t_obs >= time[nt - 1]:
                    k = nt - 1
                else:
                    for k in range(nt - 1):
                        if t_obs < time[k + 1]:
                            break

                # Calculate TDS factors:
                delta_t = (t_obs - ref_time) / 365.25  # Convert to years
                slope /= 100  # Convert to fraction per year
                tds_wa = tds_wa[0:nwl]  # Ensures all elements are valid
                factor_tds = delta_t * slope[k][0:nwl] + intercept[k][0:nwl]

                # Amend flux and error arrays:
                factor = np.interp(spec.wavelength, tds_wa, factor_tds)
                spec.flux /= factor
                spec.error /= factor

            # Append x1d spectrum to the relevant list:
            if detector[:-1] == 'NUV':
                nuv_spectra.append(spec)
            else:
                fuv_spectra.append(spec)

    if (len(nuv_spectra) == 0) | ((setup != 4) & (setup != 5)):
        spectra = [fuv_spectra]

    elif (len(fuv_spectra) == 0) | (setup == 4):
        spectra = [nuv_spectra]

    else:
        spectra = [fuv_spectra, nuv_spectra]

    print('---------------------------------------------------------')

    dispersion = [0.00997, 0.01223, 0.39]  # Grating dispersion (A/pix)

    if correlation_offset is True or scale_spectra is True:
        print('Co-aligning exposures:')

        if check_alignment is True:
            print('  Plotting before and after co-alignment snapshots')

        #################################################################
        # COALIGN DATA
        # ------------
        # We assume the CalCOS wavelength scale is relatively correct.
        # We take the following setups as a reference for each grating:
        # G130M: CENWAVE=1309A, FP-POS=3
        # G160M: CENWAVE=1600A, FP-POS=3
        # Co-alignment is on these positions if available and FP-POS=3
        # if not. If neither are available, the first exposure is used
        # as a reference.
        #
        # Data is cross-correlated on the spectral region around
        # strong ISM absorption lines. Median fluxes and errors are
        # scaled to match the median of those in the reference exposure.
        #
        # NUV data is shifted and scaled based on values in the arrays
        # 'nuv_shift' and 'nuv_scale'. Scaling and offsetting of NUV data
        # is not automated due to a lack of strong ISM lines on which
        # to cross-correlate, and because overlaps between settings are
        # not guaranteed in many setups.
        #################################################################

        # Loop over FUV and NUV spectra:
        for i in range(len(spectra)):

            # Ensure we have spectra to cross correlate:
            if len(spectra[i]) > 0:

                bestwave = ('1309', '1600')
                channame = ('G130M', 'G160M')

                #############################################
                # ISM lines used for cross-correlation:
                #
                # CII 1334.5
                # AlII 1670.8
                # SiII 1260.4
                # SiII 1526.7
                #
                # Cross-correlation region boundaries
                # defined below:

                minxcorwave = [[1330, 1664], [1255, 1520]]
                maxxcorwave = [[1340, 1676], [1266, 1533]]

                #############################################

                if (setup == 3) | (setup == 5):
                    chanind = [0, 1]

                elif setup == 4:
                    chanind = []  # Non-automated cross-correlation for G230L

                elif i == 0:
                    chanind = [setup - 1]

                if i == 1:
                    chanind = []  # Non-automated cross-correlation for G230L

                grating = np.array(
                    [spectra[i][j].header['OPT_ELEM']
                     for j in range(len(spectra[i]))])
                cenwave = np.array(
                    [spectra[i][j].header['CENWAVE']
                     for j in range(len(spectra[i]))])
                side = np.array(
                    [spectra[i][j].header['SEGMENT'][-1:]
                     for j in range(len(spectra[i]))])
                fppos = np.array(
                    [spectra[i][j].header['FPPOS']
                     for j in range(len(spectra[i]))])

                for j in chanind:

                    # Best option - centre grating setting, FP-POS=3:
                    ref = np.intersect1d(np.where(grating == channame[j])[0],
                                         np.where(cenwave == bestwave[j])[0])
                    ref = np.intersect1d(ref, np.where(fppos == 3)[0])

                    # Second-best option - anything else at FP-POS=3:
                    if len(ref) == 0:
                        ref = np.intersect1d(
                            np.where(grating == channame[j])[0],
                            np.where(fppos == 3)[0])

                    # Last option - first file:
                    if len(ref) == 0:
                        ref = np.where(grating == channame[j])
                        ref = ref[0]

                    grating0 = np.where(grating == grating[ref[0]])[0]
                    xcorr_width = 40

                    for k in grating0:

                        ref1 = np.intersect1d(
                            ref, np.where(side == side[k])[0])
                        ref1 = ref1[0]  # Use first ref file if more than one

                        if correlation_offset:

                            if side[k] == 'A':
                                refrange = (spectra[i][ref1].wavelength.value >=
                                            minxcorwave[0][j]) & \
                                           (spectra[i][ref1].wavelength.value <=
                                            maxxcorwave[0][j])
                                comprange = (spectra[i][k].wavelength.value >=
                                             minxcorwave[0][j]) & \
                                            (spectra[i][k].wavelength.value <=
                                             maxxcorwave[0][j])

                            else:
                                refrange = (spectra[i][ref1].wavelength.value >=
                                            minxcorwave[1][j]) & \
                                           (spectra[i][ref1].wavelength.value <=
                                            maxxcorwave[1][j])
                                comprange = (spectra[i][k].wavelength.value >=
                                             minxcorwave[1][j]) & \
                                            (spectra[i][k].wavelength.value <=
                                             maxxcorwave[1][j])

                            refx = spectra[i][ref1].wavelength.value[refrange]
                            compx = spectra[i][k].wavelength.value[comprange]

                            # Since the FUV spectra are oversampled by a
                            # factor ~3, we are free to smooth by 3 pixels to
                            # decrease r.m.s. for cross correlation:
                            kernel = Gaussian1DKernel(3 / 2.354820046)
                            refy = convolve(
                                spectra[i][ref1].flux[refrange], kernel)
                            compy = convolve(
                                spectra[i][k].flux[comprange], kernel)

                            if check_alignment:
                                pl.plot(refx, refy, drawstyle='steps-mid')
                                pl.plot(compx, compy, drawstyle='steps-mid')
                                pl.show()

                            shift, corr = cross_correlate(
                                refy, compy, width=xcorr_width)
                            xshift = shift * dispersion[j] * angstrom
                            spectra[i][k].wavelength += xshift

                            if check_alignment:

                                compx = spectra[i][k].wavelength.value[
                                    comprange]
                                pl.plot(refx, refy, drawstyle='steps-mid')
                                pl.plot(compx, compy, drawstyle='steps-mid')
                                pl.show()

                                apply_shift = raw_input('Apply shift? (y)/n: ')

                                if apply_shift == 'n':
                                    spectra[i][k].wavelength -= xshift
                                    print('  Offset: 0.0 Angstrom')

                                else:
                                    print('  Offset: {0}'.format(xshift))

                            if not check_alignment:
                                print('  Offset: {0}'.format(xshift))

                        if scale_spectra:
                            scale = scale_factor(
                                spectra[i][ref1].wavelength.value,
                                spectra[i][ref1].flux.value,
                                spectra[i][ref1].error.value,
                                spectra[i][k].wavelength.value,
                                spectra[i][k].flux.value,
                                spectra[i][k].error.value)
                            print('  Flux scale factor: {0}'.format(scale))
                            spectra[i][k].flux *= scale
                            spectra[i][k].error *= scale

                if ((i == 1) | (setup == 4)) & (nuv_shift is not None):

                    for j in range(len(spectra[i])):
                        print('  Offset: {0}'.format(str(nuv_shift[j])))
                        spectra[i][j].wavelength += nuv_shift[j]

                        if nuv_scale is not None:
                            print('  Flux scale '
                                  'factor: {0}'.format(str(nuv_scale[j])))
                            spectra[i][j].flux *= nuv_scale[j]
                            spectra[i][j].error *= nuv_scale[j]

    print('Applying weights, co-adding and writing new files:')

    # Loop over FUV and NUV spectra:
    for i in range(len(spectra)):

        # Apply weights:
        for j in range(len(spectra[i])):
            discard = (spectra[i][j].flags['weights'] == 0)
            de_weight = (spectra[i][j].flags['weights'] == 2)
            spectra[i][j].flux[discard] = 0.0
            spectra[i][j].error[discard] = 0.0
            spectra[i][j].exptime[discard] = 0.0
            spectra[i][j].exptime[de_weight] /= 2

        # Define array for co-added wavelength,
        # assuming a linear dispersion for the data:
        wmin = np.min([sp.wavelength.value[0] for sp in spectra[i]])
        wmax = np.max([sp.wavelength.value[-1] for sp in spectra[i]])
        if i == 1:
            wavelength = wmin + np.arange(
                (wmax - wmin) / dispersion[2] + 1) * dispersion[2]
        else:
            if setup == 1:
                wavelength = wmin + np.arange(
                    (wmax - wmin) / dispersion[0] + 1) * dispersion[0]
            elif setup == 2:
                wavelength = wmin + np.arange(
                    (wmax - wmin) / dispersion[1] + 1) * dispersion[1]
            elif setup == 4:
                wavelength = wmin + np.arange(
                    (wmax - wmin) / dispersion[2] + 1) * dispersion[2]
            else:
                # Create dual-dispersion G130M + G160M array:
                wavelength = dispersion[0] * np.arange(33099) + wmin
                good = wavelength <= 1460
                wavelength = wavelength[good]  # Truncate at 1460A
                temp = (max(wavelength) + dispersion[1] + dispersion[1] *
                        np.arange(27800))
                wavelength = np.concatenate((wavelength, temp))
                good = ((wavelength >= wmin) & (wavelength <= wmax))
                wavelength = wavelength[good]

        # Setup arrays to fill with interpolated values:
        iwavelength = np.zeros([len(wavelength), len(spectra[i])])
        iflux = np.zeros([len(wavelength), len(spectra[i])])
        ierror = np.zeros([len(wavelength), len(spectra[i])])
        iexptime = np.zeros([len(wavelength), len(spectra[i])])

        # Nearest neighbour interpolation onto new wavelength scale:
        for j in range(len(spectra[i])):
            iwavelength[:, j] = wavelength
            spec = spectra[i][j].interpolate(wavelength)
            iflux[:, j] = spec.flux
            ierror[:, j] = spec.error
            iexptime[:, j] = spec.exptime

        # Define output arrays:
        flux = np.zeros_like(wavelength)
        error = np.zeros_like(wavelength)
        exptime = np.zeros_like(wavelength)

        # Perform co-addition, looping through by pixel:
        for j in range(len(wavelength)):

            # Condition for there to be at least one good pixel:
            good = np.where(iflux[j, :] != 0)[0]
            if len(good) > 0:

                # Sum exposure times at this pixel:
                exptime[j] = np.sum(iexptime[j, good])

                # If there's only one good exposure, no co-addition required:
                if len(good) == 1:
                    flux[j] = iflux[j, good][0]
                    error[j] = ierror[j, good][0]

                # Otherwise, co-add with modified exposure weighting:
                else:
                    flux[j] = np.sum(
                        iflux[j, good] * iexptime[j, good]) / exptime[j]
                    temp = np.sum((ierror[j, good] * iexptime[j, good]) ** 2)
                    error[j] = np.sqrt(temp) / exptime[j]

        wavelength = Column(wavelength, name='WAVELENGTH', unit='Angstrom')
        flux = Column(flux, name='FLUX', unit='erg / (Angstrom cm2 s)')
        error = Column(error, name='ERROR', unit='erg / (Angstrom cm2 s)')
        spec = Table([wavelength, flux, error])

        if (setup == 1) | (setup == 2) | (setup == 3):
            filename = '{0}_COS_FUV.fits'.format(name)

        elif setup == 4:
            filename = '{0}_COS_NUV.fits'.format(name)

        elif i == 0:
            filename = '{0}_COS_FUV.fits'.format(name)

        else:
            filename = '{0}_COS_FUV.fits'.format(name)

        print('  {0}'.format(filename))

        if plot:
            print('  Plotting')
            pl.plot(spec['WAVELENGTH'], spec['FLUX'], drawstyle='steps-mid')
            pl.plot(spec['WAVELENGTH'], spec['ERROR'], drawstyle='steps-mid')
            pl.xlabel('Wavelength ($\\AA$)')
            pl.ylabel('Flux (erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$)')
            pl.show()

        spec.write(filename, overwrite=True)

        # Write individual x1d files for NUV if manual inspection required:
        if ((i == 1) | (setup == 4)) & (nuv_shift is None):
            if not os.path.lexists('x1d'):
                os.makedirs('x1d')
            for j, spec in enumerate(spectra[i]):
                filename = '{0}_x1d_new_{1}.fits'.format(
                    spec.header['ROOTNAME'], side[j])
                spec.write('x1d/{0}'.format(filename), overwrite=True)