import math
from datetime import datetime

tilesize = 24  # pixel / tile
framerate = 60  # frames / second

gravity = 40.0
air_resistance = 0.01

"""
The speed is calculated by

	new_speed = old_speed * (1-air_resitance) + gravity

Therefore the maximum speed can be calculated by

	max_speed = gravity / air_resitance

We do not want the maximum speed to be more that tilesize
becausse then collision detection would not work.
So we will adjust the framerate to catch that case:
"""

if gravity / air_resistance > framerate ** 2:
	framerate = int(math.floor(math.sqrt(gravity / air_resistance)))


# We try to adopt to different tilesizes and framerates.
# However, rounding errors may have significant influence on game physics

gravity = gravity * tilesize / framerate ** 2


def timeofday():
	t = datetime.now().time()
	return (((t.microsecond / 1000000.0 + t.second) / 60.0 + t.minute) / 60.0
		+ t.hour) / 24.0 % 1
