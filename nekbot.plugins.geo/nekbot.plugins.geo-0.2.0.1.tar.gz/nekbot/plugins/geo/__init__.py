# coding=utf-8
from geopy import Nominatim
import re
from geopy.distance import vincenty, great_circle
from nekbot.core.exceptions import InvalidArgument
from nekbot.storage.ejdb import ejdb
from nekbot.core.commands import command

__author__ = 'Nekmo'

db = ejdb('geo')
geolocator = Nominatim(timeout=5)


COORD_PATTERN = re.compile('[\+\-]?\d{1,3}\.\d{1,10},[\+\-]?\d{1,3}\.\d{1,10}')


def coord_to_tuple(coord):
    if not COORD_PATTERN.match(coord):
        raise ValueError
    coord = coord.replace('+', '')
    return map(float, coord.split(','))


def get_coord(place):
    if COORD_PATTERN.match(place):
        return coord_to_tuple(place)
    result = search(place)
    if not result:
        return None
    return float(result['lat']), float(result['lon'])


def place_coord(place):
    coord = get_coord(place)
    if coord is None:
        raise InvalidArgument('Invalid place or coord.', place)
    return coord


def search(place):
    with db.find('place', {"term": place}) as results:
        if len(results):
            return results[0]
    if COORD_PATTERN.match(place):
        location = geolocator.reverse(place.replace(',', ', '))
    else:
        location = geolocator.geocode(place)
    if location is None:
        return None
    location = location.raw
    location['term'] = place
    db.save("place", location)
    return search(place)


@command
def geo(msg, place):
    result = search(place)
    if result is None:
        return 'Sorry, no results for "%s"' % place
    result = dict(result.items())
    response = ''
    if not COORD_PATTERN.match(place):
        response += '{lat},{lon} '.format(**result)
    response += result['display_name']
    if result.get('type'):
        response += ' [%s]' % result['type']
    if result.get('osm_id') and result.get('osm_type'):
        response += ' https://www.openstreetmap.org/{osm_type}/{osm_id}'.format(**result)
    return response


@command('geodistance', place_coord, place_coord)
def geodistance(msg, place1, place2):
    return 'Vicenty distance: %fkm Great-circle distance: %fkm' % (vincenty(place1, place2).kilometers, great_circle(
        place1, place2).kilometers)