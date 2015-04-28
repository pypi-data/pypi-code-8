"""
Data and structures used by multiple unitests
"""


import os
import codecs
import json


TYPE_LOOP = (
    ('1', int),
    ('1.', float),
    ('.1', float),
    ('None', lambda x: None),
    ('False', lambda x: False),
    ('True', lambda x: True),
    ('string', str),
    ('{"K3": [0, 1, 2, 3, 4], "UPPERCASE": "v2", "k1": "MORE UPPERCASE"}', json.loads),
    (codecs.encode(os.linesep, 'unicode_escape'), lambda x: codecs.decode(x, 'unicode_escape'))
)
