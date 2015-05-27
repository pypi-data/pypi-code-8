"""Contains all inverse Fourier's Transform functions that output a 2D array"""
__author__ = 'Thomas Bealing'

import numpy
import pyfftw
import psutil
import os
from reikna.fft import FFT
from reikna import cluda

# put in __init__.py?
pyfftw.interfaces.cache.enable()
p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)


# most efficient class when all data has been collected in advance
class Direct2d(object):

    #static Reikna Setup (can be used for all input2d instances)
    api = cluda.ocl_api()
    axes = (0, 1)

    # TODO: add data validation on shape
    def __init__(self, shape):
        self.input = None

        # instance Reikna setup
        self.data = numpy.random.rand(*shape).astype(numpy.complex64)
        self.ifft_R = FFT(self.data, axes=Direct2d.axes)
        self.thr = Direct2d.api.Thread.create()
        self.fftc = self.ifft_R.compile(self.thr, fast_math=True)

        # instance FFTW setup
        self.output = pyfftw.n_byte_align_empty(shape, 16, 'complex64')

    # TODO: add data validation on array2D (should match shape)
    def ifft2D(self, array2D):
        self.input = pyfftw.n_byte_align(array2D, 16, 'complex64')
        if self.input.size >= 1024*1024:
            return self._reikna()
        else:
            return self._fftw()

    def _fftw(self):
        # print("_fftw() called")

        # FFTW Setup (requires data before this setup can run)
        ifft_F = pyfftw.FFTW(self.input, self.output, planner_effort='FFTW_ESTIMATE', direction='FFTW_BACKWARD', threads=4, axes=(0,1), planning_timelimit=0.0)

        # Run the FFT
        return ifft_F()

    def _reikna(self):
        # print("_reikna called")
        # Reikna Setup (requires data before this setup can run)
        cl_data_in = self.thr.to_device(self.input)

        # Run the FFT
        self.fftc(cl_data_in, cl_data_in, inverse=True)

        return cl_data_in.get()


# most efficient class when calculations can be performed during the scan
class OneDDecomp():
    """Calculates the inverse Fourier's transform of a 2D numpy array using 1D decomposition"""
    #static Reikna Setup (can be used for all input2d instances)
    api = cluda.ocl_api()

    # inputAxis = 0 or 1, and indicates which axis of 1d data will be entered later
    # TODO: add data validation on inputAxis
    # TODO: add data validation on shape
    def __init__(self, shape, inputAxis):
        self.input = None
        self.index2D = 0
        self.inputAxis = inputAxis

        # instance Reikna setup
        self.data = numpy.random.rand(*shape).astype(numpy.complex64)
        self.ifft_R = FFT(self.data, axes=Direct2d.axes)
        self.thr = Direct2d.api.Thread.create()
        self.fftc = self.ifft_R.compile(self.thr, fast_math=True)

        # instance FFTW setup
        self.buffer2D1 = pyfftw.n_byte_align_empty(shape, 16, 'complex64')

        # setup 1D buffer for 1D ifft output
        self.length1D = None
        if inputAxis:
            self.length1D = len(self.buffer2D1[:, 1])
        else:
            self.length1D = len(self.buffer2D1[1, :])
        self.output1DBuffer = pyfftw.n_byte_align_empty(self.length1D, 16, 'complex64')

    # TODO: add data validation on array1D (should match shape and inputAxis shape)
    def append1D(self, array1D):
        self.input = pyfftw.n_byte_align(array1D, 16, 'complex64')

        ifft = pyfftw.FFTW(self.input, self.output1DBuffer, planner_effort='FFTW_ESTIMATE', direction='FFTW_BACKWARD', threads=1, planning_timelimit=0.0)
        self.output1DBuffer = ifft()

        if self.inputAxis == 0:
            self.buffer2D1[self.index2D, :] = self.output1DBuffer
        else:
            output1DBuffer2 = self.output1DBuffer.reshape(len(self.output1DBuffer))
            self.buffer2D1[:, self.index2D] = output1DBuffer2

        self.index2D += 1

        # when all data has been received, perform 2D, 1 axis ifft
        if ((self.inputAxis == 0) and (self.index2D == len(self.buffer2D1[:, 1]))) or\
           ((self.inputAxis == 1) and (self.index2D == len(self.buffer2D1[1, :]))):
            if self.buffer2D1.size < 1024*1024:
                # FFTW
                ifft = pyfftw.FFTW(self.buffer2D1, self.buffer2D1, planner_effort='FFTW_ESTIMATE', direction='FFTW_BACKWARD', threads=4, axes=(self.inputAxis,), planning_timelimit=0.0)
                return ifft()
            else:
                # Reikna
                cl_data = self.thr.to_device(self.buffer2D1)

                # Run the FFT
                self.fftc(cl_data, cl_data, inverse=True)

                return cl_data.get()
        else:
            # Scan not finished yet
            return None