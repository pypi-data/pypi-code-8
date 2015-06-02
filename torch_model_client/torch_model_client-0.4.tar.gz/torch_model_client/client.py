import array
import requests

import numpy as np


def raw_dump_data(data):
    a = array.array('f', data)
    return a.tostring()


def raw_read_data(data):
    a = array.array('f')
    a.fromstring(data)
    return np.array(a)


def call_model(url, data):
    raw_in = raw_dump_data(data)

    raw_out = requests.post(url, raw_in).content

    return raw_read_data(raw_out)

