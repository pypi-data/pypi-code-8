""" All about Artificial star tests """
from __future__ import print_function
import argparse
import logging
import os
import sys

import matplotlib.pylab as plt
import numpy as np

from astropy.table import Table
from scipy.interpolate import interp1d

logger = logging.getLogger()

try:
    plt.style.use('ggplot')
except:
    pass

def ast_correct_starpop(filename, fake_file=None, outfile=None, overwrite=False,
                        asts_obj=None, correct_kw={}, diag_plot=False,
                        plt_kw={}, hdf5=True):
    '''
    correct mags with artificial star tests, finds filters by fake_file name

    Parameters
    ----------
    filename : trilegal catalog (must have apparent magnitudes)

    fake_file : string
         matchfake file or ANGST pipeline fake.fits file

    outfile : string
        if sgal, a place to write the table with ast_corrections

    overwrite : bool
        if sgal and outfile, overwite if outfile exists

    asts_obj : AST instance
        if not loading from fake_file

    correct_kw : dict
        passed to ASTs.correct important to consider, dxy, xrange, yrange
        see AST.correct.__doc__

    diag_plot : bool
        make a mag vs mag diff plot

    plt_kw :
        kwargs to pass to pylab.plot

    Returns
    -------
    corrected mag1 and mag2

    also adds columns to sgal.data
    '''
    sgal = StarPop(filename)
    fmt = '{}_cor'
    if asts_obj is None:
        sgal.fake_file = fake_file
        _, filter1, filter2 = parse_pipeline(fake_file)
        if fmt.format(filter1) in sgal.data.keys() or fmt.format(filter2) in sgal.data.keys():
            errfmt = '{}, {} ast corrections already in file.'
            logger.warning(errfmt.format(filter1, filter2))
            return sgal.data[fmt.format(filter1)], sgal.data[fmt.format(filter2)]
        ast = ASTs(fake_file)
    else:
        ast = asts_obj

    mag1 = sgal.data[ast.filter1]
    mag2 = sgal.data[ast.filter2]

    correct_kw = dict({'dxy': (0.2, 0.15)}.items() + correct_kw.items())
    cor_mag1, cor_mag2 = ast.correct(mag1, mag2, **correct_kw)
    names = [fmt.format(ast.filter1), fmt.format(ast.filter2)]
    data = [cor_mag1, cor_mag2]
    sgal.add_data(names, data)

    if outfile is not None:
        sgal.write_data(outfile, overwrite=overwrite, hdf5=hdf5)

    if diag_plot:
        plt_kw = dict({'color': 'navy', 'alpha': 0.3, 'label': 'sim'}.items() \
                      + plt_kw.items())
        axs = ast.magdiff_plot()
        mag1diff = cor_mag1 - mag1
        mag2diff = cor_mag2 - mag2
        rec, = np.nonzero((np.abs(mag1diff) < 10) & (np.abs(mag2diff) < 10))
        axs[0].plot(mag1[rec], mag1diff[rec], '.', **plt_kw)
        axs[1].plot(mag2[rec], mag2diff[rec], '.', **plt_kw)
        if 'label' in plt_kw.keys():
            [ax.legend(loc=0, frameon=False) for ax in axs]
        plt.savefig(replace_ext(outfile, '_ast_correction.png'))
    return cor_mag1, cor_mag2


class ASTs(object):
    '''class for reading and using artificial stars'''
    def __init__(self, filename, filter1=None, filter2=None, filt_extra=''):
        '''
        if filename has 'match' in it will assume this is a matchfake file.
        if filename has .fits extention will assume it's a binary fits table.
        '''
        self.base, self.name = os.path.split(filename)
        self.filter1 = filter1
        self.filter2 = filter2
        self.filt_extra = filt_extra

        self.target, filters = parse_pipeline(filename)
        
        try:
            self.filter1, self.filter2 = filters
        except:
            self.filter1, self.filter2, self.filter3 = filters
        self.read_file(filename)

    def recovered(self, threshold=9.99):
        '''
        find indicies of stars with magdiff < threshold

        Parameters
        ----------
        threshold: float
            [9.99] magin - magout threshold for recovery

        Returns
        -------
        self.rec: list
            recovered stars in both filters
        rec1, rec2: list, list
            recovered stars in filter1, filter2
        '''
        rec1, = np.nonzero(np.abs(self.mag1diff) < threshold)
        rec2, = np.nonzero(np.abs(self.mag2diff) < threshold)
        self.rec = list(set(rec1) & set(rec2))
        if len(self.rec) == len(self.mag1diff):
            logger.warning('all stars recovered')
        return rec1, rec2

    def make_hess(self, binsize=0.1, yattr='mag2diff', hess_kw={}):
        '''make hess grid'''
        self.colordiff = self.mag1diff - self.mag2diff
        mag = self.__getattribute__(yattr)
        self.hess = hess(self.colordiff, mag, binsize, **hess_kw)

    def read_file(self, filename):
        '''
        read MATCH fake file into attributes
        format is mag1in mag1diff mag2in mag2diff
        mag1 is assumed to be mag1in
        mag2 is assumed to be mag2in
        mag1diff is assumed to be mag1in-mag1out
        mag2diff is assumed to be mag2in-mag2out
        '''
        if 'match' in filename:
            names = ['mag1', 'mag2', 'mag1diff', 'mag2diff']
            self.data = np.genfromtxt(filename, names=names)
            # unpack into attribues
            for name in names:
                self.__setattr__(name, self.data[name])
        elif filename.endswith('.fits'):
            from astropy.io import fits
            assert not None in [self.filter1, self.filter2], \
                'Must specify filter strings'
            self.data = fits.getdata(filename)
            self.mag1 = self.data['{}_IN'.format(self.filter1)]
            self.mag2 = self.data['{}_IN'.format(self.filter2)]
            mag1out = self.data['{}{}'.format(self.filter1, self.filt_extra)]
            mag2out = self.data['{}{}'.format(self.filter2, self.filt_extra)]
            self.mag1diff = self.mag1 - mag1out
            self.mag2diff = self.mag2 - mag2out
        else:
            logger.error('{} not supported'.format(filename))

    def write_matchfake(self, newfile):
        '''write matchfake file'''
        dat = np.array([self.mag1, self.mag2, self.mag1diff, self.mag2diff]).T
        np.savetxt(newfile, dat, fmt='%.3f')

    def bin_asts(self, binsize=0.2, bins=None):
        '''
        bin the artificial star tests

        Parameters
        ----------
        bins: bins for the asts
        binsize: width of bins for the asts

        Returns
        -------
        self.am1_inds, self.am2_inds: the indices of the bins to
            which each value in mag1 and mag2 belong (see np.digitize).
        self.ast_bins: bins used for the asts.
        '''
        if bins is None:
            ast_max = np.max(np.concatenate((self.mag1, self.mag2)))
            ast_min = np.min(np.concatenate((self.mag1, self.mag2)))
            self.ast_bins = np.arange(ast_min, ast_max, binsize)
        else:
            self.ast_bins = bins

        self.am1_inds = np.digitize(self.mag1, self.ast_bins)
        self.am2_inds = np.digitize(self.mag2, self.ast_bins)

    def _random_select(self, arr, nselections):
        '''
        randomly sample arr nselections times

        Parameters
        ----------
        arr : array or list
            input to sample
        nselections : int
            number of times to sample

        Returns
        -------
        rands : array
            len(nselections) of randomly selected from arr (duplicates included)
        '''
        rands = np.array([np.random.choice(arr) for i in range(nselections)])
        return rands

    def ast_correction(self, obs_mag1, obs_mag2, binsize=0.2, bins=None,
                       not_rec_val=np.nan, missing_data1=0., missing_data2=0.):
        '''
        Apply ast correction to input mags.
        
        Corrections are made by going through obs_mag1 in bins of
        bin_asts and randomly selecting magdiff values in that ast_bin.
        obs_mag2 simply follows along since it is tied to obs_mag1.

        Random selection was chosen because of the spatial nature of
        artificial star tests. If there are 400 asts in one mag bin,
        and 30 are not recovered, random selection should match the
        distribution (if there are many obs stars).

        If there are obs stars in a mag bin where there are no asts,
        will throw the star out unless the completeness in that mag bin
        is more than 50%.
        Parameters
        ----------
        obs_mag1, obs_mag2 : N, 1 arrays
            input observerd mags

        binsize, bins : sent to bin_asts

        not_rec_val : float
            value for not recovered ast
        missing_data1, missing_data2 : float, float
            value for data outside ast limits per filter (include=0)
        
        Returns
        -------
        cor_mag1, cor_mag2: array, array
            ast corrected magnitudes

        Raises:
            returns -1 if obs_mag1 and obs_mag2 are different sizes

        To do:
        possibly return magXdiff rather than magX + magXdiff?
        reason not to: using AST results from one filter to another isn't
        kosher. At least not glatt kosher.
        '''
        self.completeness(combined_filters=True, interpolate=True)

        nstars = obs_mag1.size
        if obs_mag1.size != obs_mag2.size:
            logger.error('mag arrays of different lengths')
            return -1

        # corrected mags are filled with nan.
        cor_mag1 = np.empty(nstars)
        cor_mag1.fill(not_rec_val)
        cor_mag2 = np.empty(nstars)
        cor_mag2.fill(not_rec_val)

        # need asts to be binned for this method.
        if not hasattr(self, 'ast_bins'):
            self.bin_asts(binsize=binsize, bins=bins)
        om1_inds = np.digitize(obs_mag1, self.ast_bins)

        for i in range(len(self.ast_bins)):
            # the obs and artificial stars in each bin
            obsbin, = np.nonzero(om1_inds == i)
            astbin, = np.nonzero(self.am1_inds == i)

            nobs = len(obsbin)
            nast = len(astbin)
            if nobs == 0:
                # no stars in this mag bin to correct
                continue
            if nast == 0:
                # no asts in this bin, probably means the simulation
                # is too deep
                if self.fcomp2(self.ast_bins[i]) < 0.5:
                    continue
                else:
                    # model is producing stars where there was no data.
                    # assign correction for missing data
                    cor1 = missing_data1
                    cor2 = missing_data2
            else:
                # randomly select the appropriate ast correction for obs stars
                # in this bin
                cor1 = self._random_select(self.mag1diff[astbin], nobs)
                cor2 = self._random_select(self.mag2diff[astbin], nobs)

            # apply corrections
            cor_mag1[obsbin] = obs_mag1[obsbin] + cor1
            cor_mag2[obsbin] = obs_mag2[obsbin] + cor2
            # finite values only: not implemented because trilegal array should
            # maintain the same size.
            #fin1, = np.nonzero(np.isfinite(cor_mag1))
            #fin2, = np.nonzero(np.isfinite(cor_mag2))
            #fin = list(set(fin1) & set(fin2))
        return cor_mag1, cor_mag2

    def correct(self, obs_mag1, obs_mag2, bins=[100,200], xrange=[-0.5, 5.],
                yrange=[15., 27.], not_rec_val=0., dxy=None):
        """
        apply AST correction to obs_mag1 and obs_mag2

        Parameters
        ----------
        obs_mag1, obs_mag2 : arrays
            input mags to correct

        bins : [int, int]
            bins to pass to graphics.plotting.crazy_histogram2d

        xrange, yrange : shape 2, arrays
            limits of cmd space send to graphics.plotting.crazy_histogram2d
            since graphics.plotting.crazy_histogram2d is called twice it is
            important to have same bin sizes

        not_rec_val : float or nan
            value to fill output arrays where obs cmd does not overlap with
            ast cmd.

        dxy : array shape 2,
            color and mag step size to make graphics.plotting.crazy_histogram2d

        Returns
        -------
        cor_mag1, cor_mag2 : arrays len obs_mag1, obs_mag2
            corrections to obs_mag1 and obs_mag2
        """
        from utils import crazy_histogram2d as chist

        nstars = obs_mag1.size
        if obs_mag1.size != obs_mag2.size:
            logger.error('mag arrays of different lengths')
            return -1, -1

        # corrected mags are filled with nan.
        cor_mag1 = np.empty(nstars)
        cor_mag1.fill(not_rec_val)
        cor_mag2 = np.empty(nstars)
        cor_mag2.fill(not_rec_val)

        obs_color = obs_mag1 - obs_mag2
        ast_color = self.mag1 - self.mag2

        if dxy is not None:
            # approx number of bins.
            bins[0] = len(np.arange(*xrange, step=dxy[0]))
            bins[1] = len(np.arange(*yrange, step=dxy[1]))

        ckw = {'bins': bins, 'reverse_indices': True, 'xrange': xrange,
                    'yrange': yrange}
        SH, _, _, sixy, sinds = chist(ast_color, self.mag2, **ckw)
        H, _, _, ixy, inds = chist(obs_color, obs_mag2, **ckw)

        x, y = np.nonzero(SH * H > 0)
        # there is a way to do this with masking ...
        for i, j in zip(x, y):
            sind, = np.nonzero((sixy[:, 0] == i) & (sixy[:, 1] == j))
            hind, = np.nonzero((ixy[:, 0] == i) & (ixy[:, 1] == j))
            nobs = int(H[i, j])
            xinds = self._random_select(sinds[sind], nobs)
            cor_mag1[inds[hind]] = self.mag1diff[xinds]
            cor_mag2[inds[hind]] = self.mag2diff[xinds]

        return obs_mag1 + cor_mag1, obs_mag2 + cor_mag2

    def completeness(self, combined_filters=False, interpolate=False,
                     binsize=0.2):
        '''
        calculate the completeness of the data in each filter
        
        Parameters
        ----------
        combined_filters : bool
            Use individual or combined ast recovery
        
        interpolate : bool
            add a 1d spline the completeness function to self
        
        Returns
        -------
        self.comp1, self.comp2 : array, array
            the completeness per filter binned with self.ast_bins
        '''
        # calculate stars recovered, could pass theshold here.
        rec1, rec2 = self.recovered()

        # make sure ast_bins are good to go
        if not hasattr(self, 'ast_bins'):
            self.bin_asts(binsize=binsize)

        # gst uses both filters for recovery.
        if combined_filters is True:
            rec1 = rec2 = self.rec

        # historgram of all artificial stars
        qhist1 = np.array(np.histogram(self.mag1, bins=self.ast_bins)[0],
                          dtype=float)

        # histogram of recovered artificial stars
        rhist1 = np.array(np.histogram(self.mag1[rec1], bins=self.ast_bins)[0],
                          dtype=float)

        # completeness histogram
        self.comp1 = rhist1 / qhist1

        qhist2 = np.array(np.histogram(self.mag2, bins=self.ast_bins)[0],
                          dtype=float)
        rhist2 = np.array(np.histogram(self.mag2[rec2], bins=self.ast_bins)[0],
                          dtype=float)
        self.comp2 = rhist2 / qhist2

        if interpolate is True:
            # sometimes the histogram isn't as useful as the a spline
            # function... add the interp1d function to self.
            self.fcomp1 = interp1d(self.ast_bins[1:], self.comp1,
                                   bounds_error=False)
            self.fcomp2 = interp1d(self.ast_bins[1:], self.comp2,
                                   bounds_error=False)
        return

    def get_completeness_fraction(self, frac, dmag=0.001, bright_lim=18):
        """Find the completeness magnitude at a given fraction"""
        assert hasattr(self, 'fcomp1'), \
            'need to run completeness with interpolate=True'

        # set up array to evaluate interpolation
        # sometimes with few asts at bright mags the curve starts with low
        # completeness, reaches toward 1, and then declines as expected.
        # To get around taking a value too bright, I search for values beginning
        # at the faint end
        search_arr = np.arange(bright_lim, 31, dmag)[::-1]

        # completeness in each filter, and the finite vals
        # (frac - nan = frac)
        cfrac1 = self.fcomp1(search_arr)
        ifin1 = np.isfinite(cfrac1)
        
        cfrac2 = self.fcomp2(search_arr)
        ifin2 = np.isfinite(cfrac2)
        
        # closest completeness fraction to passed fraction
        icomp1 = np.argmin(np.abs(frac - cfrac1[ifin1]))
        icomp2 = np.argmin(np.abs(frac - cfrac2[ifin2]))

        # mag associated with completeness
        comp1 = search_arr[ifin1][icomp1]
        comp2 = search_arr[ifin2][icomp2]

        if comp1 == bright_lim or comp2 == bright_lim:
            logger.warning('Completeness fraction is at mag search limit and probably wrong. '
                           'Try adjusting bright_lim')
        return comp1, comp2

    def magdiff_plot(self, axs=None):
        """Make a plot of input mag - output mag vs input mag"""
        if not hasattr(self, 'rec'):
            self.completeness(combined_filters=True)
        if axs is None:
            fig, axs = plt.subplots(ncols=2, figsize=(12, 6))

        axs[0].plot(self.mag1[self.rec], self.mag1diff[self.rec], '.',
                    color='k', alpha=0.5)
        axs[1].plot(self.mag2[self.rec], self.mag2diff[self.rec], '.',
                    color='k', alpha=0.5)

        xlab = r'${{\rm Input}}\ {}$'

        axs[0].set_xlabel(xlab.format(self.filter1), fontsize=20)
        axs[1].set_xlabel(xlab.format(self.filter2), fontsize=20)

        axs[0].set_ylabel(r'${{\rm Input}} - {{\rm Ouput}}$', fontsize=20)
        return axs

    def completeness_plot(self, ax=None, comp_fracs=None):
        """Make a plot of completeness vs mag"""
        assert hasattr(self, 'fcomp1'), \
            'need to run completeness with interpolate=True'

        if ax is None:
            fig, ax = plt.subplots()

        ax.plot(self.ast_bins, self.fcomp1(self.ast_bins),
                label=r'${}$'.format(self.filter1))
        ax.plot(self.ast_bins, self.fcomp2(self.ast_bins),
                label=r'${}$'.format(self.filter2))
        
        if comp_fracs is not None:
            self.add_complines()
        ax.set_xlabel(r'${{\rm mag}}$', fontsize=20)
        ax.set_ylabel(r'${{\rm Completeness\ Fraction}}$', fontsize=20)
        plt.legend(loc='lower left', frameon=False)
        return ax

    def add_complines(self, ax, *fracs, **get_comp_frac_kw):
        """add verticle lines to a plot at given completeness fractions"""
        lblfmt = r'${frac}\ {filt}:\ {comp: .2f}$'
        for frac in fracs:
            ax.hlines(frac, *ax.get_xlim(), alpha=0.5)
            comp1, comp2 = self.get_completeness_fraction(frac,
                                                          **get_comp_frac_kw)
            for comp, filt in zip((comp1, comp2), (self.filter1, self.filter2)):
                lab = lblfmt.format(frac=frac, filt=filt, comp=comp)
                ax.vlines(comp, 0, 1, label=lab,
                          color=next(ax._get_lines.color_cycle))
        plt.legend(loc='lower left', frameon=False)
        return ax


def parse_pipeline(filename):
    '''find target and filters from the filename'''    
    import re
    name = os.path.split(filename)[1].upper()
    
    # filters are assumed to be F???W
    starts = np.array([m.start() for m in re.finditer('_F', name)])
    starts += 1
    if len(starts) == 1:
        starts = np.append(starts, starts+6)
    filters = [name[s: s+5] for s in starts]
    
    # the target name is assumed to be before the filters in the filename
    pref = name[:starts[0]-1]
    for t in pref.split('_'):
        if t == 'IR':
            continue
        try:
            # this could be the proposal ID
            int(t)
        except:
            # a mix of str and int should be the target
            target = t
    return target, filters


class StarPop(object):
    def __init__(self, trilegal_catalog):
        self.base, self.name = os.path.split(trilegal_catalog)
        
        if trilegal_catalog.endswith('hdf5'):
            data = Table.read(trilegal_catalog, path='data')
        else:
            #print('reading')
            data = Table.read(trilegal_catalog, format='ascii.commented_header',
                              guess=False)
            #print('read')
        self.key_dict = dict(zip(list(data.dtype.names),
                                 range(len(list(data.dtype.names)))))
        self.data = data

    def get_header(self):
        '''
        utility for writing data files, sets header attribute and returns
        header string.
        '''
        try:
            names = [k for k, v in sorted(self.key_dict.items(),
                                          key=lambda (k,v): v)]
        except AttributeError:
            names = self.data.dtype.names
        self.header = '# %s' % ' '.join(names)
        return self.header

    def add_data(self, names, data):
        '''
        add columns to self.data, update self.key_dict
        see numpy.lib.recfunctions.append_fields.__doc__

        Parameters
        ----------
        names : string, sequence
            String or sequence of strings corresponding to the names
            of the new fields.
        data : array or sequence of arrays
            Array or sequence of arrays storing the fields to add to the base.

        Returns
        -------
        header
        '''
        self.data = add_data(self.data, names, data)

        # update key_dict
        header = self.get_header()
        header += ' ' + ' '.join(names)
        col_keys = header.replace('#', '').split()
        self.key_dict = dict(zip(col_keys, range(len(col_keys))))
        return header

    def write_data(self, outfile, overwrite=False, hdf5=False):
        '''call savetxt to write self.data'''
        if not hdf5:
            savetxt(outfile, self.data, fmt='%5g', header=self.get_header(),
                           overwrite=overwrite)
        else:
            if not outfile.endswith('.hdf5'):
                outfile = replace_ext(outfile, '.hdf5')
            tbl = Table(self.data)
            tbl.write(outfile, format='hdf5', path='data', compression=True,
                      overwrite=overwrite)
            print('wrote {0:s}'.format(outfile))

        return


def hess(color, mag, binsize, **kw):
    """
    Compute a hess diagram (surface-density CMD) on photometry data.

    INPUT:
       color
       mag
       binsize -- width of bins, in magnitudes

    OPTIONAL INPUT:
       cbin=  -- set the centers of the color bins
       mbin=  -- set the centers of the magnitude bins
       cbinsize -- width of bins, in magnitudes

    OUTPUT:
       A 3-tuple consisting of:
         Cbin -- the centers of the color bins
         Mbin -- the centers of the magnitude bins
         Hess -- The Hess diagram array

    EXAMPLE:
      cbin = out[0]
      mbin = out[1]
      imshow(out[2])
      yticks(range(0, len(mbin), 4), mbin[range(0, len(mbin), 4)])
      xticks(range(0, len(cbin), 4), cbin[range(0, len(cbin), 4)])
      ylim([ylim()[1], ylim()[0]])

    2009-02-08 23:01 IJC: Created, on a whim, for LMC data (of course)
    2009-02-21 15:45 IJC: Updated with cbin, mbin options
    2012 PAR: Gutted and changed it do histogram2d for faster implementation.
    """
    defaults = dict(mbin=None, cbin=None, verbose=False)

    for key in defaults:
        if (not kw.has_key(key)):
            kw[key] = defaults[key]

    if kw['mbin'] is None:
        mbin = np.arange(mag.min(), mag.max(), binsize)
    else:
        mbin = np.array(kw['mbin']).copy()
    if kw['cbin'] is None:
        cbinsize = kw.get('cbinsize')
        if cbinsize is None:
            cbinsize = binsize
        cbin = np.arange(color.min(), color.max(), cbinsize)
    else:
        cbin = np.array(kw['cbin']).copy()

    hesst, cbin, mbin = np.histogram2d(color, mag, bins=[cbin, mbin])
    hess = hesst.T
    return (cbin, mbin, hess)


def savetxt(filename, data, fmt='%.4f', header=None, overwrite=False,
            loud=False):
    '''
    np.savetxt wrapper that adds header. Some versions of savetxt
    already allow this...
    '''
    if overwrite is True or not os.path.isfile(filename):
        with open(filename, 'w') as f:
            if header is not None:
                if not header.endswith('\n'):
                    header += '\n'
                f.write(header)
            np.savetxt(f, data, fmt=fmt)
        if loud:
            print('wrote', filename)
    else:
        logging.error('%s exists, not overwriting' % filename)
    return


def replace_ext(filename, ext):
    '''
    input
    filename string with .ext
    new_ext replace ext with new ext
    eg:
    $ replace_ext('data.02.SSS.v4.dat', '.log')
    data.02.SSS.v4.log
    '''
    return split_file_extention(filename)[0] + ext


def split_file_extention(filename):
    '''
    split the filename from its extension
    '''
    return '.'.join(filename.split('.')[:-1]), filename.split('.')[-1]


def add_data(old_data, names, new_data):
    '''
    use with Starpop, Track, or any object with data attribute that is a
    np.recarray

    add columns to self.data, update self.key_dict
    see numpy.lib.recfunctions.append_fields.__doc__

    Parameters
    ----------
    old_data : recarray
        original data to add columns to

    new_data : array or sequence of arrays
        new columns to add to old_data

    names : string, sequence
        String or sequence of strings corresponding to the names
        of the new_data.

    Returns
    -------
    array with old_data and new_data
    '''
    import numpy.lib.recfunctions as nlr
    data = nlr.append_fields(np.asarray(old_data), names, new_data).data
    data = data.view(np.recarray)
    return data


def crazy_histogram2d(x, y, bins=10, weights=None, reduce_w=None, NULL=None,
                      reinterp=None, reverse_indices=False, xrange=None,
                      yrange=None):
    """
    Written by Morgan Foresneau

    Compute the sparse bi-dimensional histogram of two data samples where *x*,
    and *y* are 1-D sequences of the same length. If *weights* is None
    (default), this is a histogram of the number of occurences of the
    observations at (x[i], y[i]).

    If *weights* is specified, it specifies values at the coordinate (x[i],
    y[i]). These values are accumulated for each bin and then reduced according
    to *reduce_w* function, which defaults to numpy's sum function (np.sum).
    (If *weights* is specified, it must also be a 1-D sequence of the same
    length as *x* and *y*.)

    Parameters
    ----------
    x: ndarray[ndim=1]
        first data sample coordinates

    y: ndarray[ndim=1]
        second data sample coordinates

    bins: int or [int, int], optional
        the bin specification
        `int`       : the number of bins for the two dimensions (nx=ny=bins)
        `[int, int]`: the number of bins in each dimension (nx, ny = bins)

    weights: ndarray[ndim=1], optional
        values *w_i* weighing each sample *(x_i, y_i)*, they will be
        accumulated and reduced (using reduced_w) per bin

    reduce_w: callable, optional (default=np.sum)
        function that will reduce the *weights* values accumulated per bin
        defaults to numpy's sum function (np.sum)

    NULL: value type, optional
        filling missing data value

    reinterp: str in [None, 'nn', linear'], optional
        if set, reinterpolation is made using mlab.griddata to fill missing
        data within the convex polygone that encloses the data

    reverse_indices: bool, option
        also return the bins of each x, y point as a 2d array

    Returns
    -------
    B: ndarray[ndim=2]
        bi-dimensional histogram

    extent: tuple(4)
        (xmin, xmax, ymin, ymax) entension of the histogram

    steps: tuple(2)
        (dx, dy) bin size in x and y direction

    """
    # define the bins (do anything you want here but needs edges and sizes of the 2d bins)
    try:
        nx, ny = bins
    except TypeError:
        nx = ny = bins

    #values you want to be reported
    if weights is None:
        weights = np.ones(x.size)

    if reduce_w is None:
        reduce_w = np.sum
    else:
        if not hasattr(reduce_w, '__call__'):
            raise TypeError('reduce function is not callable')

    # culling nans
    finite_inds = (np.isfinite(x) & np.isfinite(y) & np.isfinite(weights))
    _x = np.asarray(x)[finite_inds]
    _y = np.asarray(y)[finite_inds]
    _w = np.asarray(weights)[finite_inds]

    if not (len(_x) == len(_y)) & (len(_y) == len(_w)):
        raise ValueError('Shape mismatch between x, y, and weights: {}, {}, {}'.format(_x.shape, _y.shape, _w.shape))
    if xrange is None:
        xmin, xmax = _x.min(), _x.max()
    else:
        xmin, xmax = xrange
    if yrange is None:
        ymin, ymax = _y.min(), _y.max()
    else:
        ymin, ymax = yrange
    inds, = np.nonzero((_x > xmin) & (_x < xmax) & (_y > ymin) & (_y < ymax))
    _x = _x[inds]
    _y = _y[inds]
    _w = _w[inds]

    dx = (xmax - xmin) / (nx - 1.0)
    dy = (ymax - ymin) / (ny - 1.0)

    # Basically, this is just doing what np.digitize does with one less copy
    xyi = np.vstack((_x, _y)).T
    xyi -= [xmin, ymin]
    xyi /= [dx, dy]
    xyi = np.floor(xyi, xyi).T

    #xyi contains the bins of each point as a 2d array [(xi,yi)]

    d = {}
    for e, k in enumerate(xyi.T):
        key = (k[0], k[1])

        if key in d:
            d[key].append(_w[e])
        else:
            d[key] = [_w[e]]

    _xyi = np.array(d.keys()).T
    _w   = np.array([ reduce_w(v) for v in d.values() ])

    # exploit a sparse coo_matrix to build the 2D histogram...
    _grid = sparse.coo_matrix((_w, _xyi), shape=(nx, ny))

    if reinterp is None:
        #convert sparse to array with filled value
        ## grid.toarray() does not account for filled value
        ## sparse.coo.coo_todense() does actually add the values to the existing ones, i.e. not what we want -> brute force
        if NULL is None:
            B = _grid.toarray()
        else:  # Brute force only went needed
            B = np.zeros(_grid.shape, dtype=_grid.dtype)
            B.fill(NULL)
            for (x, y, v) in zip(_grid.col, _grid.row, _grid.data):
                B[y, x] = v
    else:  # reinterp
        xi = np.arange(nx, dtype=float)
        yi = np.arange(ny, dtype=float)
        B = griddata(_grid.col.astype(float), _grid.row.astype(float),
                     _grid.data, xi, yi, interp=reinterp)

    if reverse_indices:
        return B, (xmin, xmax, ymin, ymax), (dx, dy), xyi.T, inds

    return B, (xmin, xmax, ymin, ymax), (dx, dy)


