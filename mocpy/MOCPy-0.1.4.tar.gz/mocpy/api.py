#!/usr/bin/env python
# -*- coding: utf-8 -*

"""

api.py:
  provides the main functions to read and write MOCs

"""

from moc import MOC_io, MOC

__author__ = "Thomas Boch"
__copyright__ = "CDS, Centre de Données astronomiques de Strasbourg"

def new(max_norder):
    """
    Creates a new MOC object
    """
    return MOC(max_norder)

def read(path):
    """
    Load a MOC from a URL or a local file path
    """
    path = path.strip()
    if path.startswith('http'):
        # utiliser astropy.utils.data.download_file
        pass
    else:
        return MOC_io.read_local(path)
    


    

def filter_list(moc, pos_list, keep_inside=True):
    """
    Filter a list of sources
    """
    pass
    

if __name__ == '__main__':
    #from astroquery.vizier import Vizier
    #Vizier.ROW_LIMIT = -1
    
    #table = Vizier.get_catalogs('I/293/npm2cros')[0]
    #moc = MOC.from_file('/data/MOC/examples/P-GALEXGR6-AIS-FUV.fits')
    #moc = MOC.from_file('/data/MOC/examples/P-ULTRAVISTA-Ks.fits')
    moc = MOC.from_file('/data/MOC/examples/P-CFHTLS-W-r.fits')

    print(moc.sky_fraction)

    #t = moc.query_vizier('I/239/hip_main', max_rows=-1)
    #t = moc.query_simbad(max_rows=100000)
    #print t
    
    #filtered_table = moc.filter_table(table, '_RAJ2000', '_DEJ2000', keep_inside=False)
