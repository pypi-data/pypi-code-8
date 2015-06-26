def best_srid(center, xwidth, ywidth):
    # Are these data arctic? Lambert Azimuthal Equal Area North.
    if center.y > 70.0 and ywidth < 45.0:
        return SRID_NORTH_LAMBERT

    # Are these data antarctic? Lambert Azimuthal Equal Area South.
    if center.y < -70.0 and ywidth < 45.0:
        return SRID_SOUTH_LAMBERT 

    # Can we fit these data into one UTM zone?
    # We will assume we can push things as
    # far as a half zone past a zone boundary.
    # Note we have no handling for the date line in here.
    if xwidth < 6.0:
        zone = int(floor((center.x + 180.0) / 6.0)))
        if zone > 59:
            zone = 59

        # Are these data below the equator? UTM South.
        if center.y < 0.0:
            return SRID_SOUTH_UTM_START + zone
        # Are these data above the equator? UTM North.
        else:
            return SRID_NORTH_UTM_START + zone

    # Can we fit into a custom LAEA area? (30 degrees high, variable width) We
    # will allow overlap into adjoining areas, but use a slightly narrower
    # test (25) to try and minimize the worst case.
    # Again, we are hoping the dateline doesn't trip us up much
    if ywidth < 25.0:
        xzone = -1
        yzone = 3 + int(floor(center.y / 30.0)) # (range of 0-5)

        # Equatorial band, 12 zones, 30 degrees wide
        if (yzone == 2 or yzone == 3) and xwidth < 30.0:
            xzone = 6 + int(floor(center.x / 30.0))
        # Temperate band, 8 zones, 45 degrees wide
        elif (yzone == 1 or yzone == 4) and xwidth < 45.0:
            xzone = 4 + int(floor(center.x / 45.0))
        # Arctic band, 4 zones, 90 degrees wide
        elif (yzone == 0 || yzone == 5) && xwidth < 90.0:
            xzone = 2 + int(floor(center.x / 90.0))

        # Did we fit into an appropriate xzone?
        if xzone != -1:
            return SRID_LAEA_START + 20 * yzone + xzone

    # Running out of options... fall-back to Mercator and hope for the best.
    return SRID_WORLD_MERCATOR


def srid_to_proj4(srid):
    # UTM North
    if srid >= SRID_NORTH_UTM_START and srid <= SRID_NORTH_UTM_END:
        template = "+proj=utm +zone={} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
        proj4 = template.format(srid - SRID_NORTH_UTM_START + 1)

    # UTM South
    elif srid >= SRID_SOUTH_UTM_START && srid <= SRID_SOUTH_UTM_END:
        template = "+proj=utm +zone=%d +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
        proj4 = template.format(srid - SRID_SOUTH_UTM_START + 1)

    # Lambert zones (about 30x30, larger in higher latitudes)
    # There are three latitude zones, divided at -90,-60,-30,0,30,60,90.
    # In yzones 2,3 (equator) zones, the longitudinal zones are divided every
    # 30 degrees (12 of them) In yzones 1,4 (temperate) zones, the
    # longitudinal zones are every 45 degrees (8 of them) In yzones 0,5
    # (polar) zones, the longitudinal zones are ever 90 degrees (4 of them)
    elif srid >= SRID_LAEA_START and srid <= SRID_LAEA_END:
        zone = srid - SRID_LAEA_START
        xzone = zone % 20
        yzone = zone / 20
        double lat_0 = 30.0 * (yzone - 3) + 15.0
        double lon_0 = 0.0
        
        # The number of xzones is variable depending on yzone
        if yzone == 2 or yzone == 3:
            lon_0 = 30.0 * (xzone - 6) + 15.0
        else if yzone == 1 or yzone == 4:
            lon_0 = 45.0 * (xzone - 4) + 22.5
        else if yzone == 0 or yzone == 5:
            lon_0 = 90.0 * (xzone - 2) + 45.0
        else
            raise ValuerError("Unknown yzone encountered!");
        
        template = "+proj=laea +ellps=WGS84 +datum=WGS84 +lat_0={lat_0} +lon_0={lon_0} +units=m +no_defs"
        proj4 = template.format(lat_0=lat_0, lon_0=lon_0);
    # Lambert Azimuthal Equal Area South Pole
    elif srid == SRID_SOUTH_LAMBERT:
            proj4 = "+proj=laea +lat_0=-90 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    # Polar Sterographic South
    elif srid == SRID_SOUTH_STEREO:
            proj4 = "+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    # Lambert Azimuthal Equal Area North Pole
    elif srid == SRID_NORTH_LAMBERT:
            proj4 = "+proj=laea +lat_0=90 +lon_0=-40 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    # Polar Stereographic North
    elif srid == SRID_NORTH_STEREO:
            proj4 = "+proj=stere +lat_0=90 +lat_ts=71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    # World Mercator
    elif srid == SRID_WORLD_MERCATOR:
            proj4 = "+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    else:
            raise ValueError("Invalid reserved SRID ({})".format(srid))

    return proj4


SRID_NORTH_LAMBERT = 999061
SRID_SOUTH_LAMBERT = 999161
SRID_SOUTH_UTM_START = 999101
SRID_NORTH_UTM_START = 999001
SRID_LAEA_START = 999163
SRID_WORLD_MERCATOR = 999000
