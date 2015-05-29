import pygame

"""
A gradient function is one that is given a number
between 0 and 1 and returns a color.

This module should provide some way to dynamically
generate gradient functions based on some parameters.
"""


def gradient_factory(color1, color2, exponent=1):
	"""Return a linear interpolation function between color1 and color2.

	>>> c1 = pygame.color.Color(0, 0, 0, 255)
	>>> c2 = pygame.color.Color(255, 255, 255, 255)
	>>> gradient = gradient_factory(c1, c2)
	>>> gradient(0)
	(0, 0, 0, 255)
	>>> gradient(1)
	(255, 255, 255, 255)
	>>> gradient(0.5)
	(127, 127, 127, 255)
	"""

	r = lambda x: int(color1.r * (1 - x) + color2.r * x)
	g = lambda x: int(color1.g * (1 - x) + color2.g * x)
	b = lambda x: int(color1.b * (1 - x) + color2.b * x)
	a = lambda x: int(color1.a * (1 - x) + color2.a * x)

	_gradient = lambda x: pygame.color.Color(r(x), g(x), b(x), a(x))
	gradient = lambda x: _gradient(x ** exponent)

	return gradient


def _interpolation_factory(*floats):
	"""Interpolate between an arbitrary number of numbers.

	Each argument may be a number or a tuple of two numbers. The second number in
	the tuple can be used to manipulate the distribution of the numbers in the
	interpolation function.

	>>> fn = _interpolation_factory((1, 2), 2, 4)
	>>> round(fn(0) * 10)
	11.0
	>>> round(fn(0.5) * 10)
	18.0
	>>> round(fn(0.667) * 10)
	21.0
	>>> round(fn(1) * 10)
	37.0
	"""

	widths = [i[1] if isinstance(i, tuple) else 1 for i in floats]
	floats = [i[0] if isinstance(i, tuple) else i for i in floats]

	centers = [0]
	for i in range(len(widths) - 1):
		centers.append(centers[-1] + (widths[i] + widths[i + 1]) / 2.0)
	full_width = centers[-1]

	def curve_factory(center, width):
		return lambda x: 1 / (1 + abs((float(x) - center) * 2 / width) ** 3)

	curves = [curve_factory(centers[i], widths[i]) for i in range(len(floats))]

	def interpolation(rate):
		factors = [c(rate * full_width) for c in curves]
		return sum([floats[i] * factors[i]
			for i in range(len(floats))]) / sum(factors)

	return interpolation


def _mix_factory(*colors):
	"""mix multiple colors."""

	colors = [i if isinstance(i, tuple) else (i, 1) for i in colors]

	r = _interpolation_factory(*[(c[0].r, c[1]) for c in colors])
	g = _interpolation_factory(*[(c[0].g, c[1]) for c in colors])
	b = _interpolation_factory(*[(c[0].b, c[1]) for c in colors])
	a = _interpolation_factory(*[(c[0].a, c[1]) for c in colors])

	return lambda x: pygame.color.Color(int(r(x)), int(g(x)), int(b(x)),
		int(a(x)))


class Background(object):
	"""Background gradient generator based on time of day.

	>>> gradient = Background.gradient(0)
	>>> gradient(0)
	(16, 17, 25, 255)
	"""

	backgrounds = [
		{  # night
			'top': pygame.color.Color(15, 15, 20, 255),
			'bottom': pygame.color.Color(30, 10, 80, 255),
			'exponent': 1,
			'duration': (6 - 0) * 2,
		},
		{  # morning
			'top': pygame.color.Color(60, 190, 220, 255),
			'bottom': pygame.color.Color(80, 230, 80, 255),
			'exponent': 1.6,
			'duration': 10 - 6,
		},
		{  # noon
			'top': pygame.color.Color(50, 30, 160, 255),
			'bottom': pygame.color.Color(60, 170, 200, 255),
			'exponent': 1,
			'duration': 17 - 10,
		},
		{  # dawn
			'top': pygame.color.Color(220, 80, 180, 255),
			'bottom': pygame.color.Color(50, 80, 180, 255),
			'exponent': 0.7,
			'duration': 19 - 17,
		},
		{  # twilight
			'top': pygame.color.Color(140, 30, 40, 255),
			'bottom': pygame.color.Color(30, 10, 100, 255),
			'exponent': 0.8,
			'duration': 22 - 19,
		},
		{  # night
			'top': pygame.color.Color(15, 15, 20, 255),
			'bottom': pygame.color.Color(30, 10, 80, 255),
			'exponent': 1,
			'duration': (24 - 22) * 2,
		},
	]

	color1 = staticmethod(_mix_factory(
		*[(bg['top'], bg['duration']) for bg in backgrounds]))
	color2 = staticmethod(_mix_factory(
		*[(bg['bottom'], bg['duration']) for bg in backgrounds]))
	exponent = staticmethod(_interpolation_factory(
		*[(bg['exponent'], bg['duration']) for bg in backgrounds]))

	@classmethod
	def gradient(cls, timeofday):
		return gradient_factory(cls.color1(timeofday), cls.color2(timeofday),
			exponent=cls.exponent(timeofday))


def draw(img, gradient):
	h = img.get_height()
	w = img.get_width()

	for y in range(h):
		color = gradient(y / float(h))
		pygame.draw.line(img, color, (0, y), (w - 1, y))
