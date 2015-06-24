import json
import re
import requests
import logging
from .endpoint import EndPoint as ep

class Client():
    def __init__(self, host, port="4242"):
        self.host = host
        self.port = port

    @staticmethod
    def _assert_status(r, expected):
        if r.status_code != expected:
            logging.critical(r.text)
            raise requests.ConnectionError("Expected status code {0}, but got {1}".format(expected, r.status_code))

    def _uri(self, ep):
        return "http://{0}:{1}{2}".format(self.host, self.port, ep)

    def put(self, metrics):
        r = requests.post(self._uri(ep.put), data=json.dumps(metrics))
        self._assert_status(r, 204)

    def aggregators(self):
        r = requests.get(self._uri(ep.aggregators))
        self._assert_status(r, 200)
        return json.loads(r.text)

    def lookup(self, metric="", tags={}):
        if(metric == "" and not tags):
            return []
        m = metric
        if tags:
            m += "{"
            for key in tags:
                m += "{0}={1}".format(key, tags[tag])
                m += ","
            m = m[:-1]
            m += "}"
        params = { "m": m }

        r = requests.get(self._uri(ep.lookup), params=params)
        self._assert_status(r, 200)
        return json.loads(r.text)

    def lookup_uids(self, metric="", tags={}):
        r = self.lookup(metric, tags)
        uids = []
        for result in r["results"]:
            uids.append(result["tsuid"])
        return uids

