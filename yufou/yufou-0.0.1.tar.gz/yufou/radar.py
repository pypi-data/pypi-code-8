# coding: utf-8

'''
    yufou.radar
    ~~~~~~~~~~~

    Retrieve radar stat.
'''

from datetime import datetime, timedelta

from yufou.data.radar import from_city, from_radar_no


def round_to_5_minutes(moment):
    '''Round datetime to 5 minutes boundary:

    - if moment.minute < 5 -> moment.minute = 0
    - if moment.minute >= 5 -> moment.minute = 0

    :param moment: a :class:`datetime.datetime` instance.
    '''
    return moment - timedelta(minutes=moment.minute % 5, seconds=moment.second)


def image(radar, at=None):
    '''Retrieve a radar image.

    :param radar: radar station no.
    :param at: stat datetime, defaults to now.
    '''
    at = round_to_5_minutes(at or datetime.utcnow())

    return ''.join([
        'http://image.nmc.cn/product',
        '/{0}'.format(at.year),
        '/{0}'.format(at.strftime('%Y%m')),
        '/{0}'.format(at.strftime('%Y%m%d')),
        '/RDCP/medium/SEVP_AOC_RDCP_SLDAS_EBREF_',
        '{0}_L88_PI_'.format(radar),
        '{0}00000.GIF'.format(at.strftime('%Y%m%d%H%M'))
    ])


def radar_station_from_city(name):
    '''Get a radar station from city name.

    :param name: city name.
    '''
    return from_city.get(name)


def radar_station_from_radar_no(no):
    '''Get a radar station from no.

    :param no: radar no.
    '''
    return from_radar_no.get(no)
