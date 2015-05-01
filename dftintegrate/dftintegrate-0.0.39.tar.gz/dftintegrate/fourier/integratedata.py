"""
Classes::
  IntegrateData -- The IntegrateData class is a collection of
    functions that integrate the fit created by FitData.
"""

import numpy as np

from itertools import product
from json import load, dump
from scipy.special.orthogonal import p_roots

from ..customserializer import tojson, fromjson
from dftintegrate.fourier import fitdata


class IntegrateData(object):
    """Integrate the fourier representation of a 3D function contained in
    fit.json.

    Variables::
      data -- Data to integrate represented in fit.json.

      points -- Number of integration points i.e. number of rectangles.

    Functions::
      set_(recips, coeffs, num, bandnum) --
        Set (recips, coeffs, num, bandnum) in case
        loaddata is false. Intended use is for testing.

      _integrate -- Call the functions to run the integration scheme.

      _evaluatefit -- Take the Fourier representation of the band and
        evaluate it at the integration points.

      _rectangleintegral -- Use the 3D analogue of the midpoint rule to
        integrate the Fourier representation of a band.

      _gaussintegral -- Use Gaussian Quadrature to integrate the Fourier
        representation of a band.

      rectangles -- Loop through the calculated bands and call
        _rectangleintegral.

      gauss -- Loop through the calculated bands and call _gaussintegral.

      serialize -- Serialize the integration to a json file.

    """
    def __init__(self, name_of_directory, points, loaddata=True,
                 integrate=True, bandnum='all'):
        """
        Arguments::
          name_of_directory -- path to directory that contains fit.json.

          points -- Number of integration points i.e. number of
            rectangles.

        Keyword Arguments::
          loaddata -- Boolean that says to automatically load data from
            fit.json. This is useful if I want to test only one function.
            Default True.

          integrate -- Boolean that says to automatically run _integrate.
            This is useful if I want to test only one function. Also
            determines auto serialize. Default True.

          bandnum -- Number of bands to fit. Default is to integrate all
            bands in fit.json.
        """
        self.name = name_of_directory
        self.points = int(points)
        self.bandnum = bandnum
        if loaddata:
            with open(self.name+'fit.json', mode='r',
                      encoding='utf-8') as inf:
                self.data = load(inf, object_hook=fromjson)
            self.recips = self.data['reciprocals']
            self.coeffs = self.data['coefficients']
        self.rectangleintegrals = []
        self.gaussintegrals = []
        if integrate:
            self._integrate()

    def set_recips(self, recips):
        self.recips = recips

    def set_coeffs(self, coeffs):
        self.coeffs = coeffs

    def set_num(self, num):
        self.num = num

    def set_bandnum(self, bandnum):
        self.bandnum = bandnum

    def set_points(self, points):
        self.points = points

    def _integrate(self):
        self.rectangles()
        self.gauss()
        self.serialize()

    def _evaluatefit(self, A=None):
        """
        Use A x = b to solve for b.
        """
        if A is None:
            fitdata.FitData.gen_series(self)
            A = self.series
        print("Things being stored in dictionaries is messing up the dot product I think because the order changes so the answer comes out different all the time.")
        return(np.dot(A, self.coeffs[self.num]))

    def _rectangleintegral(self, b=None):
        """Since we are integrating a 3D function this isn't technically
        rectangle method, but it is the same idea. The whole idea is
        to make a bunch of cubes that tile space then evaluate the
        function at the center of each cube and add them up and call
        that the integral.
        """
        if b is None:
            b = self._evaluatefit()
        divs = len(b)
        volume = 1/divs
        integral = sum(b*volume)
        self.rectangleintegrals.append(integral)

    def _gaussintegral(self):
        """
        Integrate over the interval 0 to 1/2 then multiply by 8 (2 cubed),
        since we have even functions. Evaluate the fit on that kgid,
        multiply function value by the weights.

        """
        b = self._evaluatefit()
        integral = 8*np.power((self.end-self.start)/2,
                              3)*sum(np.multiply(b, self.weights))
        self.gaussintegrals.append(integral)

    def rectangles(self):
        """Generate a grid to evaluate the function on, the points will be
        used as the midpoints for our rectangle rule. Then run the
        loops according to how many bands we are calculating.

        """
        self.kgrid = [x for x in
                      product([i/self.points for i in range(self.points)],
                              repeat=3)]
        if self.bandnum == 'all':
            for num in range(1, len(self.coeffs.keys())+1):
                self.num = str(num)
                self._rectangleintegral()
        else:
            for num in range(1, self.bandnum+1):
                self.num = str(num)
                self._rectangleintegral()

    def gauss(self):
        """
        Integrate over the interval 0 to 1/2. Generate the grid to
        evaluate the function on with scipy.special.orthogonal's
        p_roots, also generates the weights. p_roots gave the gauss
        points in 1d so we make kgrid 3D with itertools.product, then
        shift from 0 to 1, to, 0 to 1/2. Similarly make the weights
        3D. Then run the loops according to haw many bands we are
        calculating.

        """
        self.start = 0
        self.end = 0.5
        self.kgrid, self.weights = p_roots(self.points)
        self.kgrid = np.real(self.kgrid)
        self.kgrid = np.asarray([x for x in product(self.kgrid, repeat=3)])
        self.kgrid = (self.end-self.start)*(self.kgrid+1)/2.0 + self.start
        self.weights = np.asarray([np.product(x) for x in
                                   product(self.weights, repeat=3)])
        if self.bandnum == 'all':
            for num in range(1, len(self.coeffs.keys())+1):
                self.num = str(num)
                self._gaussintegral()
        else:
            for num in range(1, self.bandnum+1):
                self.num = str(num)
                self._gaussintegral()

    def serialize(self):
        integral_dict = {'rectangleintegrals': self.rectangleintegrals,
                         'totalrectangleintegral': sum(self.rectangleintegrals),
                         'gaussintegrals': self.gaussintegrals,
                         'totalgaussintegral': sum(self.gaussintegrals)}
        with open(self.name+'integral.json', mode='w',
                  encoding='utf-8') as outf:
            dump(integral_dict, outf, indent=2, default=tojson)
