# - * - coding:utf8 - * -

# primarycolors is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# primary colors is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with primarycolors.  If not, see <http://www.gnu.org/licenses/>.


import operator
import six
from scipy.misc import imread, imresize
from scipy.cluster.vq import kmeans, vq
from scipy import histogram, array, sum as adder, product


class PrimaryColors(object):

    def __init__(self, image=None, max_colors=5, optimum=True):

        """Determination of the primary colors in an image file.
        :param: image - a path to image.
        :param: max_colors - the maximum number of colors in the resulting.
        :param: optimum - allows you to reduce the images for optimization performance.
        """

        # Convert image into array of values for each point.
        ar = imread(image)

        # If size image is big, then reduce size for optimization performance
        if optimum and ar.shape[0] > 50 and ar.shape[1] > 50:
            ar = imresize(ar, (50, 50))

        shape = ar.shape
        # Reshape array of values to merge color bands.
        if len(shape) > 2:
            ar = ar.reshape(product(shape[:2]), shape[2])
        # Get max_colors worth of centroids.
        ar = ar.astype(float)
        codes = kmeans(ar, max_colors)[0]
        # Pare centroids, removing blacks and whites and shades of really dark and really light.
        original_codes = codes
        for low, hi in [(60, 200), (35, 230), (10, 250)]:
            codes = array([code for code in codes
                           if not ((code[0] < low and code[1] < low and code[2] < low) or
                                   (code[0] > hi and code[1] > hi and code[2] > hi))])
            if not len(codes):
                codes = original_codes
            else:
                break
        # Assign codes (vector quantization). Each vector is compared to the centroids
        # and assigned the nearest one.
        vectors = vq(ar, codes)[0]
        # Count occurences of each clustered vector.
        self.__counts = histogram(vectors, len(codes))[0]
        self.__codes = codes.astype(int)
        # Show colors for each code in its hex value.

    @staticmethod
    def __to_hsl(rgb_tuple):
        """
        :param rgb tuple:
        :return: hsl tuple.
        """
        r, g, b = rgb_tuple
        r_h, g_h, b_h = [x/255.0 for x in rgb_tuple]
        c_max = max(r_h, g_h, b_h)
        c_min = min(r_h, g_h, b_h)
        maximum = max(rgb_tuple)
        minimum = min(rgb_tuple)

        if maximum == minimum:
            h = 0
        elif maximum == r and g >= b:
            h = 60 * (g - b)/(maximum - minimum)
        elif maximum == r and g < b:
            h = 60 * (g - b)/(maximum - minimum) + 360
        elif maximum == g:
            h = 60 * (b - r)/(maximum - minimum) + 120
        else:
            h = 60 * (r - g)/(maximum - minimum) + 240
        l = 50 * (c_max + c_min)
        s = (c_max - c_min) / (1 - abs(1 - (c_max + c_min))) * 100
        return h, s, l

    @property
    def hex(self):

        """The primary colors in the RGB hexadecimal array."""

        colors = [''.join([hex(int(x))[2:] for x in rgb]) for rgb in self.__codes]
        return colors

    @property
    def rgb(self):

        """The primary colors in the RGB integer array."""

        return self.__codes.tolist()

    @property
    def web(self):

        """The primary colors in the array with web-prefix."""

        colors = self.hex
        return ['#%s' % c for c in colors]

    @property
    def sorted_colors(self):

        """An array of primary colors with the frequency coefficients."""

        total = adder(self.__counts)
        colors = self.hex
        color_dist = dict(zip(colors, [count/float(total) for count in self.__counts]))
        color_sorted = sorted(six.iteritems(color_dist), key=operator.itemgetter(1), reverse=True)
        return color_sorted

    @property
    def hsl(self):

        """The primary colors in the HSL array."""

        return [self.__to_hsl(c) for c in self.__codes]
