"""The JSONDataHandler handles all JSON data needed for making
recommendations."""
from data_handler import DataHandler
from urllib import parse
from urllib import request
import json
import contextlib


class JSONDataHandler(DataHandler):
    """Handle all JSON data needed for recommendations"""

    def __init__(self, source):
        self._source = source

    def get_content(self):
        raise NotImplementedError

    def get_top_matching_items(self, item, limit):
        raise NotImplementedError

    def update_top_matching_items(self, top_matches):
        raise NotImplementedError

    def _fetch_data(self, path):
        """Fetches JSON encoded data and returns it as a dictionary.
        When for some reason fetching data is impossible a
        ConnectionRefusedError or an URLError is thrown.

        parameters:
            path The at which the resource can be reached"""
        data = request.Request(self._source + path)
        with contextlib.closing(request.urlopen(data)) as response:
            json_data = response.read().decode("utf-8")
        return json.loads(json_data)

    def _post_data(self, data, path, key="data"):
        """Posts JSON encoded data to a given path.
        When for some reason posting data is impossible a
        ConnectionRefusedError or an URLError is thrown.

        parameters:
            data The data to post
            path The path at which the data should be posted
            key The POST parameter name to use. Default is data"""
        data = parse.urlencode({key: json.dumps(data)})

        update_request = request.Request(self._source + path)
        update_request.add_header("Content-Type",
                                  "application/json;charset=utf-8")
        with contextlib.closing(request.urlopen(update_request,
                                                data.encode("utf-8"))):
            pass
