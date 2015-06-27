# coding: utf-8

'''
    yufou.data.radar
    ~~~~~~~~~~~~~~~~

    Radar stations data.
'''

import os
import json


__all__ = ['from_city', 'from_radar_no']


DATA_FILE = os.path.join(os.path.dirname(__file__), 'radar.json')


from_city = {}
from_radar_no = {}
with open(DATA_FILE) as f:
    for station in json.load(f):
        from_city[station['city']] = station.copy()
        from_radar_no[station['radar']] = station.copy()
