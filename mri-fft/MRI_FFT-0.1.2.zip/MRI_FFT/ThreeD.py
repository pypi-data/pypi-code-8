"""For use when a 3D output array is required.

It includes two classes:

- "Direct3d", for when all of the k-space data is available immediately, and
- "TwoDDecomp", or two-dimensional decomposition, for when two dimensional k-space data can be processed during the scan.
"""
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
class Direct3d(object):
    """Calculates the inverse Fourier's transform of a 3D numpy array directly

    This class should be used when all of the data is available immediately.

    :param shape: The shape of the 3D array that contains the k-space data to be transformed
    :type shape: 1D array

    .. note:: Memory errors can occur with large array sizes.
    """

    # static Reikna Setup (can be used for all input2d instances)
    __api = cluda.any_api()
    __axes = (0, 1, 2)

    def __init__(self, shape):
        """Direct3D Constructor: Initializes pyFFTW and Reikna

        :param shape: The shape of the 3D array that contains the k-space data to be transformed
        :type shape: 1D array
        """
        if len(shape) != 3:
            raise ValueError('Invalid Shape: Expected a tuple of length 3')
        self.input = None
        self.shape = shape

        # instance FFTW setup
        self.output = pyfftw.n_byte_align_empty(shape, 16, 'complex64')

    def ifft3D(self, array3D):
        """Calculates the 3D inverse Fourier's Transform of array3D

        :param array3D: An array of k-space data
        :type array3D: A complex or real 3D numpy array
        :return: The transformed array
        :rtype: A complex64 3D numpy array
        """

        if self.shape != array3D.shape:
            raise ValueError('array3D has an unexpected shape')

        self.input = pyfftw.n_byte_align(array3D, 16, 'complex64')
        if self.input.size <= 256*256*256:
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
        # instance Reikna setup
        self.data = numpy.random.rand(*self.shape).astype(numpy.complex64)
        self.ifft_R = FFT(self.data, axes=Direct3d.__axes)
        self.thr = Direct3d.__api.Thread.create()
        self.fftc = self.ifft_R.compile(self.thr, fast_math=True)

        # print("_reikna called")
        # Reikna Setup (requires data before this setup can run)
        cl_data_in = self.thr.to_device(self.input)

        # Run the FFT
        self.fftc(cl_data_in, cl_data_in, inverse=True)

        return cl_data_in.get()


# most efficient class when calculations can be performed during the scan
class TwoDDecomp(object):
    """Calculates the inverse Fourier's transform of a 3D numpy array using 2D decomposition

    This class should be used when 2D data becomes available during the 3D scan.

    :param shape: The shape of the 3D array that contains the k-space data to be transformed
    :param inputAxis: The direction in which to append the 2D arrays.
        For example, for inputAxis == 0, the arrays will be entered as follows [0, :, :], [1, :, :], etc
    :type shape: 2D array
    :type inputAxis: Integer: 0, 1, or 2

    .. note:: Memory errors can occur with large array sizes.
    """
    # static Reikna Setup (can be used for all input2d instances)
    __api = cluda.ocl_api()

    # inputAxis = 0 or 1, and indicates which axis of 1d data will be entered later

    def __init__(self, shape, inputAxis):
        """TwoDDecomp Constructor: Initializes pyFFTW and Reikna

        :param shape: The shape of the 3D array that contains the k-space data to be transformed
        :param inputAxis: The direction in which to append the 2D arrays.
            For example, for inputAxis == 0, the arrays will be entered as follows [0, :, :], [1, :, :], etc
        :type shape: 2D array
        :type inputAxis: Integer: 0, 1, or 2
        """

        if len(shape) != 3:
            raise ValueError('Invalid Shape: Expected a tuple of length 3')

        if inputAxis != 0 and inputAxis != 1 and inputAxis != 2:
            raise ValueError('Invalid Axis: Expected 0, 1, or 2')

        self.input = None
        self.index2D = 0
        self.inputAxis = inputAxis

        # instance 3D FFTW setup
        self.buffer3D1 = pyfftw.n_byte_align_empty(shape, 16, 'complex64')

        # instance 2D Reikna setup
        if inputAxis == 0:
            self.shape2D = numpy.array([shape[1], shape[2]])
        elif inputAxis == 1:
            self.shape2D = numpy.array([shape[0], shape[2]])
        else:
            self.shape2D = numpy.array([shape[0], shape[1]])
        self.data2d = numpy.random.rand(*self.shape2D).astype(numpy.complex64)
        self.ifft_R2d = FFT(self.data2d, axes=(0, 1))
        self.thr2d = TwoDDecomp.__api.Thread.create()
        self.fftc2d = self.ifft_R2d.compile(self.thr2d, fast_math=True)

        # instance 2D FFTW setup
        self.output2DBuffer = pyfftw.n_byte_align_empty(self.shape2D, 16, 'complex64')

    def append2D(self, array2D):
        """Calculates the 2D iFFT, then appends it to the 3D array.

        When the last 2D array is entered, the 3D iFFT is calculated and returned.

        :param array2D: An array of k-space data
        :type array2D: A complex or real 2D numpy array
        :return: The transformed complete array
        :rtype: A complex64 3D numpy array

        .. note:: 2D arrays must be entered in order
        """

        if self.inputAxis == 0 and self.buffer3D1[0, :, :].shape != array2D.shape:
            raise ValueError('Invalid Shape: Expected a 2D numpy array of shape ', self.buffer3D1[0, :, :].shape)
        elif self.inputAxis == 1 and self.buffer3D1[:, 0, :].shape != array2D.shape:
            raise ValueError('Invalid Shape: Expected a 2D numpy array of shape ', self.buffer3D1[:, 0, :].shape)
        elif self.inputAxis == 2 and self.buffer3D1[:, :, 0].shape != array2D.shape:
            raise ValueError('Invalid Shape: Expected a 2D numpy array of shape ', self.buffer3D1[:, :, 0].shape)

        self.input = pyfftw.n_byte_align(array2D, 16, 'complex64')

        if array2D.shape[0]*array2D.shape[1] < 1024*1024:
            ifft2d = pyfftw.FFTW(self.input, self.output2DBuffer, planner_effort='FFTW_ESTIMATE', direction='FFTW_BACKWARD', axes=(0, 1), threads=1, planning_timelimit=0.0)
            self.output2DBuffer = ifft2d()
        else:
            data_in = self.thr2.to_device(self.input)

            # Run the FFT
            self.fftc2d(data_in, data_in, inverse=True)

            self.output2DBuffer = data_in.get()

        if self.inputAxis == 0:
            self.buffer3D1[self.index2D, :, :] = self.output2DBuffer
        elif self.inputAxis == 1:
            self.buffer3D1[:, self.index2D, :] = self.output2DBuffer
        else:
            self.buffer3D1[:, :, self.index2D] = self.output2DBuffer
        self.index2D += 1

        # when all data has been received, perform 2D, 1 axis ifft
        if ((self.inputAxis == 0) and (self.index2D == len(self.buffer3D1[:, 1, 1]))) or\
           ((self.inputAxis == 1) and (self.index2D == len(self.buffer3D1[1, :, 1]))) or\
           ((self.inputAxis == 2) and (self.index2D == len(self.buffer3D1[1, 1, :]))):
            if self.buffer3D1.size > 256*256*256:
                # FFTW
                print('3D FFTW')
                ifft = pyfftw.FFTW(self.buffer3D1, self.buffer3D1, planner_effort='FFTW_ESTIMATE', direction='FFTW_BACKWARD', threads=4, axes=(self.inputAxis,), planning_timelimit=0.0)
                return ifft()
            else:
                # Reikna
                print('3D Reikna')
                # instance 3D Reikna setup
                self.data = numpy.random.rand(*self.buffer3D1.shape).astype(numpy.complex64)
                self.ifft_R = FFT(self.data, axes=(self.inputAxis,))
                self.thr = TwoDDecomp.__api.Thread.create()
                self.fftc = self.ifft_R.compile(self.thr, fast_math=True)

                cl_data = self.thr.to_device(self.buffer3D1)

                # Run the FFT
                self.fftc(cl_data, cl_data, inverse=True)

                return cl_data.get()
        else:
            # Scan not finished yet
            return None