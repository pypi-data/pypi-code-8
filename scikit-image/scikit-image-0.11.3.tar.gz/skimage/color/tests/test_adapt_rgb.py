from functools import partial

import numpy as np

from skimage import img_as_float, img_as_uint
from skimage import color, data, filters
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage._shared._warnings import expected_warnings

# Down-sample image for quicker testing.
COLOR_IMAGE = data.astronaut()[::5, ::5]
GRAY_IMAGE = data.camera()[::5, ::5]

SIGMA = 3
smooth = partial(filters.gaussian_filter, sigma=SIGMA)
assert_allclose = partial(np.testing.assert_allclose, atol=1e-8)


@adapt_rgb(each_channel)
def edges_each(image):
    return filters.sobel(image)


@adapt_rgb(each_channel)
def smooth_each(image, sigma):
    return filters.gaussian_filter(image, sigma)


@adapt_rgb(hsv_value)
def edges_hsv(image):
    return filters.sobel(image)


@adapt_rgb(hsv_value)
def smooth_hsv(image, sigma):
    return filters.gaussian_filter(image, sigma)


@adapt_rgb(hsv_value)
def edges_hsv_uint(image):
    with expected_warnings(['precision loss']):
        return img_as_uint(filters.sobel(image))


def test_gray_scale_image():
    # We don't need to test both `hsv_value` and `each_channel` since
    # `adapt_rgb` is handling gray-scale inputs.
    assert_allclose(edges_each(GRAY_IMAGE), filters.sobel(GRAY_IMAGE))


def test_each_channel():
    filtered = edges_each(COLOR_IMAGE)
    for i, channel in enumerate(np.rollaxis(filtered, axis=-1)):
        expected = img_as_float(filters.sobel(COLOR_IMAGE[:, :, i]))
        assert_allclose(channel, expected)


def test_each_channel_with_filter_argument():
    filtered = smooth_each(COLOR_IMAGE, SIGMA)
    for i, channel in enumerate(np.rollaxis(filtered, axis=-1)):
        assert_allclose(channel, smooth(COLOR_IMAGE[:, :, i]))


def test_hsv_value():
    filtered = edges_hsv(COLOR_IMAGE)
    value = color.rgb2hsv(COLOR_IMAGE)[:, :, 2]
    assert_allclose(color.rgb2hsv(filtered)[:, :, 2], filters.sobel(value))


def test_hsv_value_with_filter_argument():
    filtered = smooth_hsv(COLOR_IMAGE, SIGMA)
    value = color.rgb2hsv(COLOR_IMAGE)[:, :, 2]
    assert_allclose(color.rgb2hsv(filtered)[:, :, 2], smooth(value))


def test_hsv_value_with_non_float_output():
    # Since `rgb2hsv` returns a float image and the result of the filtered
    # result is inserted into the HSV image, we want to make sure there isn't
    # a dtype mismatch.
    filtered = edges_hsv_uint(COLOR_IMAGE)
    filtered_value = color.rgb2hsv(filtered)[:, :, 2]
    value = color.rgb2hsv(COLOR_IMAGE)[:, :, 2]
    # Reduce tolerance because dtype conversion.
    assert_allclose(filtered_value, filters.sobel(value), rtol=1e-5, atol=1e-5)
