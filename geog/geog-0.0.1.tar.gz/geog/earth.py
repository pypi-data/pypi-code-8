import pyproj

wgs84 = pyproj.Geod(ellps='WGS84')
sphere = pyproj.Geod(ellps='sphere')  # Default Proj4 r: 6370997.0 meters

def spherical(r):
    g = pyproj.Geod(ellps='sphere', a=r, b=r)
    return g
