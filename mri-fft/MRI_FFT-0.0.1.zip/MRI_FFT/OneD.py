"""Contains all inverse Fourier's Transform functions that output a 1D array"""
__author__ = 'Thomas Bealing'

import numpy
import pyfftw
import psutil
import os

pyfftw.interfaces.cache.enable()
p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)


class Direct1d(object):


   # TODO: add data validation on array1D
    def ifft1D(self, array1D):
        """Return a numpy array containing the 1D inverse Fourier's Transform of array1D"""
        input = pyfftw.n_byte_align(array1D, 16, 'complex64')

        # FFTW Setup (requires data before this setup can run)
        ifft_F = pyfftw.FFTW(input, input, planner_effort='FFTW_ESTIMATE', direction='FFTW_BACKWARD', threads=1, axes=(0,), planning_timelimit=0.0)

        # Run the FFT
        return ifft_F()