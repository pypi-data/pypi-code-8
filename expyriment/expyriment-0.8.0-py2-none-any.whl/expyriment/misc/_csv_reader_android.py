"""An emulation of the csv.reader module.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = '0.8.0'
__revision__ = '19b141b'
__date__ = 'Tue Jun 30 17:14:58 2015 +0200'


def reader(the_file):
    '''
    This is a 'dirty' emulation of the csv.reader module only used for 
    Expyriment loading designs under Android. The function reads in a csv file
    and returns a 2 dimensional array.
    
    Parameters
    ----------
    the_file: iterable
        The file to be parsed.
    
    Notes
    -----
    It is strongly suggested the use, if possible, the csv package from the 
    Python standard library.
   
    
    '''
    delimiter = ","
    rtn = []
    for row in the_file:
        rtn.append(map(lambda strn: strn.strip(), row.split(delimiter)))
    return rtn

