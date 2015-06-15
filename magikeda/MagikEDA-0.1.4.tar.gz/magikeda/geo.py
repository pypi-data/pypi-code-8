# -*- coding: utf-8 -*-
"""
Functions to plot maps and coordinates.

"""


from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import gc

import pandas as pd


def plot_path_from_above(lon, lat, padding=2., show_map=True, color='red', connect_points=False, aspect_ratio=3./4, ax=None):
    """

    Parameters
    ----------
        lon : pd.Series
            Series containing the list of longitudes.

        lat : pd.Series
            Series containing the list of latitudes.

        padding : float
            Space to add arond path (in degrees). Default is 2 degrees.

        show_map : boolean
            Whether to draw the map around the path. Default is True.

        color : color or list of colors.
            The color of the path. Default is red. Optionally, if the parameter connect_poiints is False, a list of colors
            can be passed (having the same size as the number of dots). Example:
            >> colors = plt.cm.get_cmap('coolwarm', numbr_of_colors)
            >> color_idx = [ int(i) for i in color_values ]
            >> geo.plot_path_from_above(lon, lat, color=colors(color_idxs))

        connect_points : float
            Whether to connect the dots composing the path. Default is False.

        aspect_ratio : float or str or tuple
            Aspect ration of the map. Default is 3/4. The values 'square' and 'fit_extremities' can also be specified. The first
            creates a square map. The second, adds just enough space to fit the extremities (still adding the padding). The corrdinates
            of the box containing the map can also be specified as (min_lat, max_lat, min_lon, max_lon).

        ax : AxesSubplot
            Axes where to plot the map.

    """

    # Determine min and max longitude and latitude and add padding around them
    min_lat = lat.min() - padding * 3/4 # The fator 3/4 is needed to take into account the different scales between longitudes and latitudes
    max_lat = lat.max() + padding * 3/4
    min_lon = lon.min() - padding
    max_lon = lon.max() + padding


    # Determine the rightmost point of the graph
    if aspect_ratio=='fit_extremities':

        # The rightmost point is just the max lat added with the padding
        max_lat = max_lat

    elif aspect_ratio=='square':

        # The rightmost point the the that make the map a squared box
        max_lat = min_lat + np.abs(max_lon - min_lon) * 3/4 # The 3/4 is need to take into account the different scales between longitudes and latitudes

    elif isinstance(aspect_ratio, float):

        # We reduce some space from the latitude dimension to make the map obey the aspect ration given in the parameter aspect_ratio
        max_lat = min_lat + np.abs(max_lon - min_lon) * 3/4
        min_lat = min_lat + np.abs(max_lat - min_lat) * (0.5 - aspect_ratio/2) # make the min_lat a little higher
        max_lat = max_lat - np.abs(max_lat - min_lat) * (0.5 - aspect_ratio/2) # make the max_lat a little lower

    elif len(aspect_ratio)==4:

        # Get the coordinates provided
        min_lat, max_lat, min_lon, max_lon = aspect_ratio

    else:
        raise Exception('Invalid value for parameter aspect_ratio: %s' % aspect_ratio)


    # Create map centered around the path
    m = Basemap(projection='merc',
        resolution = 'l', area_thresh = 1,
        llcrnrlon= min_lon,
        urcrnrlon= max_lon,
        llcrnrlat= min_lat,
        urcrnrlat= max_lat
    )

    # Draw map, if specified
    if show_map:

        # Draw paralles and meridians
        m.drawparallels(np.arange(-80.,81.,2.))
        m.drawmeridians(np.arange(-180.,181.,2.))

        # Draw relief and rivers
        m.shadedrelief()
        m.drawrivers()

    # Draw path
    if connect_points:
        m.plot(lon.values, lat.values, latlon=True, color=color, ax=ax)
    else:
        m.scatter(lon.values, lat.values, latlon=True, color=color, ax=ax)

    gc.collect()

if __name__=='__main__':

    pass

