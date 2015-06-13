# -*- coding: utf-8 -*-
"""Copyright 2014 Roger R Labbe Jr.

filterpy library.
http://github.com/rlabbe/filterpy

Documentation at:
https://filterpy.readthedocs.org

Supporting book at:
https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python

This is licensed under an MIT license. See the readme.MD file
for more information.
"""


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
from scipy.linalg import inv
from numpy import dot, zeros, eye
from filterpy.common import dot3, dot4, dotn


class FixedLagSmoother(object):
    """ Fixed Lag Kalman smoother.

    Computes a smoothed sequence from a set of measurements based on the
    fixed lag Kalman smoother. At time k, for a lag N, the fixed-lag smoother
    computes the state estimate for time k-N based on all measurements made
    between times k-N and k. This yields a pretty good smoothed result with
    O(N) extra computations performed for each measurement. In other words,
    if N=4 this will consume about 5x the number of computations as a
    basic Kalman filter. However, the loops contain only 3 dot products, so it
    will be much faster than this sounds as the main Kalman filter loop
    involves transposes and inverses, as well as many more matrix
    multiplications.

    Implementation based on Wikipedia article as it existed on
    November 18, 2014.


    **Example**::

        fls = FixedLagSmoother(dim_x=2, dim_z=1)

        fls.x = np.array([[0.],
                          [.5]])

        fls.F = np.array([[1.,1.],
                          [0.,1.]])

        fls.H = np.array([[1.,0.]])

        fls.P *= 200
        fls.R *= 5.
        fls.Q *= 0.001

        zs = [...some measurements...]
        xhatsmooth, xhat = fls.smooth_batch(zs, N=4)


    **References**

    Wikipedia http://en.wikipedia.org/wiki/Kalman_filter#Fixed-lag_smoother

    Simon, Dan. "Optimal State Estimation," John Wiley & Sons pp 274-8 (2006).

    |
    |

    **Methods**
    """


    def __init__(self, dim_x, dim_z, N=None):
        """ Create a fixed lag Kalman filter smoother. You are responsible for
        setting the various state variables to reasonable values; the defaults
        below will not give you a functional filter.

        **Parameters**

        dim_x : int
            Number of state variables for the Kalman filter. For example, if
            you are tracking the position and velocity of an object in two
            dimensions, dim_x would be 4.

            This is used to set the default size of P, Q, and u

        dim_z : int
            Number of of measurement inputs. For example, if the sensor
            provides you with position in (x,y), dim_z would be 2.

        N : int, optional
            If provided, the size of the lag. Not needed if you are only
            using smooth_batch() function. Required if calling smooth()
        """

        self.dim_x = dim_x
        self.dim_z = dim_z
        self.N     = N

        self.x = zeros((dim_x,1)) # state
        self.x_s = zeros((dim_x,1)) # smoothed state
        self.P = eye(dim_x)       # uncertainty covariance
        self.Q = eye(dim_x)       # process uncertainty
        self.F = 0                # state transition matrix
        self.H = 0                # Measurement function
        self.R = eye(dim_z)       # state uncertainty
        self.K = 0                # kalman gain
        self.residual = zeros((dim_z, 1))

        self.B = 0
        self.PCol     = np.zeros((N+1, dim_x, dim_x))
        self.PCol_old = np.zeros((N+1, dim_x, dim_x))
        self.PS       = np.zeros((N+1, dim_x, dim_x))
        self.PS_old   = np.zeros((N+1, dim_x, dim_x))

        # identity matrix. Do not alter this.
        self._I = np.eye(dim_x)

        self.count = 0

        if N is not None:
            self.xSmooth = []



    def smooth(self, z, u=None):
        """ Smooths the measurement using a fixed lag smoother.

        On return, self.xSmooth is populated with the N previous smoothed
        estimates,  where self.xSmooth[k] is the kth time step. self.x
        merely contains the current Kalman filter output of the most recent
        measurement, and is not smoothed at all (beyond the normal Kalman
        filter processing).

        self.xSmooth grows in length on each call. If you run this 1 million
        times, it will contain 1 million elements. Sure, we could minimize
        this, but then this would make the caller's code much more cumbersome.

        This also means that you cannot use this filter to track more than
        one data set; as data will be hopelessly intermingled. If you want
        to filter something else, create a new FixedLagSmoother object.

        **Parameters**

        z : ndarray or scalar
            measurement to be smoothed


        u : ndarray, optional
            If provided, control input to the filter
        """

        # take advantage of the fact that np.array are assigned by reference.
        H = self.H
        R = self.R
        F = self.F
        P = self.P
        x = self.x
        Q = self.Q
        B = self.B
        N = self.N

        k = self.count

        # predict step of normal Kalman filter
        x_pre = dot(F, x)
        if u is not None:
            x_pre += dot(B,u)

        P = dot3(F, P, F.T) + Q

        # update step of normal Kalman filter
        y = z - dot(H, x_pre)

        S = dot3(H, P, H.T) + R
        SI = inv(S)

        K = dot3(P, H.T, SI)

        x = x_pre + dot(K, y)

        I_KH = self._I - dot(K, H)
        P = dot3(I_KH, P, I_KH.T) + dot3(K, R, K.T)

        self.xSmooth.append(x_pre.copy())

        #compute invariants
        HTSI = dot(H.T, SI)
        F_LH = (F - dot(K,H)).T

        if k >= N:
            PS = P.copy() # smoothed P for step i
            for i in range (N):
                K = dot(PS, HTSI)  # smoothed gain
                PS = dot(PS, F_LH) # smoothed covariance

                si = k-i
                self.xSmooth[si] = self.xSmooth[si] + dot(K, y)
        else:
            # Some sources specify starting the fix lag smoother only
            # after N steps have passed, some don't. I am getting far
            # better results by starting only at step N.
           self.xSmooth[k] = x.copy()

        self.count += 1
        self.x = x
        self.P = P



    def smooth_batch(self, zs, N, us=None):
        """ batch smooths the set of measurements using a fixed lag smoother.
        I consider this function a somewhat pedalogical exercise; why would
        you not use a RTS smoother if you are able to batch process your data?
        Hint: RTS is a much better smoother, and faster besides. Use it.

        This is a batch processor, so it does not alter any of the object's
        data. In particular, self.x is NOT modified. All date is returned
        by the function.

        **Parameters**


        zs : ndarray of measurements

            iterable list (usually ndarray, but whatever works for you) of
            measurements that you want to smooth, one per time step.

        N : int
           size of fixed lag in time steps

        us : ndarray, optional

            If provided, control input to the filter for each time step


        **Returns**

        (xhat_smooth, xhat) : ndarray, ndarray

            xhat_smooth is the output of the N step fix lag smoother
            xhat is the filter output of the standard Kalman filter
        """


        # take advantage of the fact that np.array are assigned by reference.
        H = self.H
        R = self.R
        F = self.F
        P = self.P
        x = self.x
        Q = self.Q
        B = self.B

        if x.ndim == 1:
            xSmooth = zeros((len(zs), self.dim_x))
            xhat    = zeros((len(zs), self.dim_x))
        else:
            xSmooth = zeros((len(zs), self.dim_x, 1))
            xhat    = zeros((len(zs), self.dim_x, 1))
        for k, z in enumerate(zs):

            # predict step of normal Kalman filter
            x_pre = dot(F, x)
            if us is not None:
                x_pre += dot(B,us[k])

            P = dot3(F, P, F.T) + Q

            # update step of normal Kalman filter
            y = z - dot(H, x_pre)

            S = dot3(H, P, H.T) + R
            SI = inv(S)

            K = dot3(P, H.T, SI)

            x = x_pre + dot(K, y)

            I_KH = self._I - dot(K, H)
            P = dot3(I_KH, P, I_KH.T) + dot3(K, R, K.T)

            xhat[k]    = x.copy()
            xSmooth[k] = x_pre.copy()

            #compute invariants
            HTSI = dot(H.T, SI)
            F_LH = (F - dot(K,H)).T

            if k >= N:
                PS = P.copy() # smoothed P for step i
                for i in range (N):
                    K = dot(PS, HTSI)  # smoothed gain
                    PS = dot(PS, F_LH) # smoothed covariance

                    si = k-i
                    xSmooth[si] = xSmooth[si] + dot(K, y)
            else:
                # Some sources specify starting the fix lag smoother only
                # after N steps have passed, some don't. I am getting far
                # better results by starting only at step N.
                xSmooth[k] = xhat[k]

        return xSmooth, xhat


    def smooth_simon(self, z, u=0):
        """ Smooths the measurement using a fixed lag smoother.

        On return, self.xSmooth is populated with the N previous smoothed
        estimates,  where self.xSmooth[k] is the kth time step. self.x
        merely contains the current Kalman filter output of the most recent
        measurement, and is not smoothed at all (beyond the normal Kalman
        filter processing).

        self.xSmooth grows in length on each call. If you run this 1 million
        times, it will contain 1 million elements. Sure, we could minimize
        this, but then this would make the caller's code much more cumbersome.

        This also means that you cannot use this filter to track more than
        one data set; as data will be hopelessly intermingled. If you want
        to filter something else, create a new FixedLagSmoother object.

        **Parameters**

        z : ndarray or scalar
            measurement to be smoothed


        u : ndarray, optional
            If provided, control input to the filter
        """


         # take advantage of the fact that np.array are assigned by reference.
        H = self.H
        R = self.R
        F = self.F
        Q = self.Q
        B = self.B
        N = self.N

        self.x = dot(F, self.x) + dot(B, u)


        y = z - dot(H, self.x)
        S = dot3(H, self.P, H.T) + R # innovation covariance
        invS = inv(S)

        L = dot4(F, self.P, H.T, invS)

        self.x += dot(L, y)
        self.x_s = self.x.copy()

        self.PCol_old[0] = self.P
        self.PS_old[0] = self.P

        self.P -= dot4(L, H, self.P, F.T) + Q

        if self.count >= N:
            for i in range(N):
                KSmooth = dot3(self.PCol_old[i], H.T, invS)
                self.PS[i+1] = self.PS_old[i] - dot4(self.PCol_old[i], H.T, L.T, F.T)
                self.PCol[i+1] = dot(self.PCol_old[i], (F - dot(L, H)).T)
                self.x_s += dot(KSmooth, y)

        self.PS_old[:, :, :] = self.PS
        self.PCol_old[:, :, :] = self.PCol

        self.count += 1


if __name__ == "__main__":
    from numpy.random import randn
    import matplotlib.pyplot as plt

    dt = 1.
    kf2 = FixedLagSmoother(2, 1, 3)

    kf2.x = np.array([[1., 1.]]).T
    kf2.F = np.array([[1, dt],
                     [0, 1.]])
    kf2.H = np.array([[1., 0]])
    kf2.Q *= 0.0001
    kf2.R *= 1.

    kfo = FixedLagSmoother(2, 1, 3)

    kfo.x = np.array([[1., 1.]]).T
    kfo.F = np.array([[1, dt],
                     [0, 1.]])
    kfo.H = np.array([[1., 0]])
    kfo.Q *= 0.0001
    kfo.R *= 1.

    from filterpy.kalman import KalmanFilter
    kf = KalmanFilter(2, 1)
    kf.x = np.array([[1., 1.]]).T
    kf.F = np.array([[1, dt],
                     [0, 1.]])
    kf.H = np.array([[1., 0]])
    kf.Q *= 0.0001
    kf.R *= 1.

    xs, xs2, zs = [], [], []
    xold = []
    for x in range(2, 50):
        z = x + randn()
        zs.append(z)

        kf2.smooth_simon(z)
        xs2.append(kf2.x_s.copy())

        kfo.smooth(z)
        xold.append(kfo.x.copy())

        kf.predict()
        kf.update(z)
        xs.append(kf.x.copy())

    z = np.array(z)
    xs = np.array(xs)
    xold = np.array(xold)
    xs2 = np.array(xs2)

    plt.plot(xs[:,0])
    plt.plot(xs2[:,0], label='simon')
    plt.plot(zs, 'r')
    plt.plot(list(range(2,50)), 'k')
    plt.legend()

    plt.plot(xold[:,0], 'p')

    z_true = np.array(list(range(2, 50)))

    dkf = z_true-xs.T[:,0][0]
    dkf2 = z_true-xs2.T[:,0][0]
    dold = z_true-xold.T[:,0][0]


