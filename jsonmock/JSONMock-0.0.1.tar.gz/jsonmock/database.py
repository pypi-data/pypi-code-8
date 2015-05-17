__author__ = 'anass'

import unittest
import json
from JSONtoObject.wrapper import Wrapper, wrap


class Database(object):

    def __init__(self, json_file):
        with open(json_file) as fp:
            self.location = json_file
            self.data = wrap(json.load(fp))

    def save(self):
        with open(self.location, "w+") as fp:
            fp.write(json.dumps(self.data.to_json()))