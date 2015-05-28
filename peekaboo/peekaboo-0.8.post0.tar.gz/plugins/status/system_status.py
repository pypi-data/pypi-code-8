#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def load_avg_status():
    data = {}

    loadavg = os.getloadavg()
    data['system.load_avg_1min'] = loadavg[0]
    data['system.load_avg_5min'] = loadavg[1]
    data['system.load_avg_15min'] = loadavg[2]
    return data

if __name__ == "__main__":
    print load_avg_status()
