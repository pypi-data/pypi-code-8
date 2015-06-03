"""
eveparser.parsers.fitting
~~~~~~~~~~~~~~~~~~~~~~~~
Parse saved fittings.

"""
from eveparser.exceptions import Unparsable
from eveparser.parsers.listing import parse_listing


FITTING_BLACKLIST = ['High power',
                     'Medium power',
                     'Low power',
                     'Rig Slot',
                     'Sub System',
                     'Charges',
                     'Drones',
                     'Fuel']


def parse_fitting(lines):
    """ Parse Fitting List

    :param string paste_string: A new-line separated list of items
    """

    if any([True for line in lines if line in FITTING_BLACKLIST]):
        lines = [line for line in lines if line not in FITTING_BLACKLIST]
    else:
        raise Unparsable('Not a fitting list')

    return parse_listing(lines)
