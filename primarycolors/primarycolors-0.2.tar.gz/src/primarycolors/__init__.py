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
import exceptions
from scipy.misc import imread
from scipy.cluster.vq import kmeans, vq
from scipy import histogram, array, sum as s, product


class PrimaryColors(object):

    def __init__(self, image, max_colors=5):

        """Determination of the primary colors in an image file.
        :param: image - a path to image.
        :param: max_colors - the maximum number of colors in the resulting.
        """

        # Convert image into array of values for each point.
        ar = imread(image)
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
        vecs = vq(ar, codes)[0]
        # Count occurences of each clustered vector.
        counts = histogram(vecs, len(codes))[0]

        # Show colors for each code in its hex value.
        self.codes = codes.astype(int)
        self.colors = [''.join(chr(c) for c in code).encode('hex') for code in self.codes]
        total = s(counts)
        color_dist = dict(zip(self.colors, [count/float(total) for count in counts]))
        self.color_sorted = sorted(color_dist.iteritems(), key=operator.itemgetter(1), reverse=True)

    @property
    def get_hex_colors(self):
        """
        :return: The primary colors in the RGB hexadecimal array
        """
        return self.colors

    @property
    def get_int_colors(self):
        """
        :return: The primary colors in the RGB integer array
        """
        return self.codes

    @property
    def get_sorted_colors(self):
        """
        :return: An array of primary colors with the frequency coefficients.
        """
        return self.color_sorted
