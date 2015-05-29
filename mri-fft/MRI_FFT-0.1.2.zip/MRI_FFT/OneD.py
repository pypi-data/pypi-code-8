"""For use when a 1D output array is required.

It contains a single class:

- "Direct1d", for directly calculating the inverse Fourier's Transform
"""
__author__ = 'Thomas Bealing'

import numpy
import pyfftw
import psutil
import os

pyfftw.interfaces.cache.enable()
p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)


class Direct1d(object):
    """Calculates the inverse Fourier's transform of a 1D numpy array directly"""

   # TODO: add data validation on array1D
    def ifft1D(self, array1D):
        """Calculates the 1D inverse Fourier's Transform of array1D

        :param array1D: An array of k-space data
        :type array1D: A complex or real 1D numpy array
        :return: The transformed array
        :rtype: A complex64 1D numpy array
        """
        if len(array1D.shape) != 1:
            raise ValueError('Invalid array1D: Expected a 1D numpy array')

        input = pyfftw.n_byte_align(array1D, 16, 'complex64')

        # FFTW Setup (requires data before this setup can run)
        ifft_F = pyfftw.FFTW(input, input, planner_effort='FFTW_ESTIMATE', direction='FFTW_BACKWARD', threads=1, axes=(0,), planning_timelimit=0.0)

        # Run the FFT
        return ifft_F()