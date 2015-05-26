import os

from gcodeutils.gcoder import GCode

__author__ = 'olivier'


def open_gcode_file(filename):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)) as gcode:
        return GCode(gcode.readlines())
