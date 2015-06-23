import logging
import json
import urllib2


class Client(object):

    """Netuitive Rest Api Client for agent data ingest.

    Posts Element data to Netuitive Cloud

    Args:
        url: The URL for the Netuitive Cloud API
        api_keys: The API key provided by your Netuitive Cloud Data Source

    """

    def __init__(self, url='https://api.app.netuitive.com/ingest',
                 api_key='apikey'):
        if url.endswith('/'):
            url = url[:-1]

        self.url = url
        self.api_key = api_key

    def post(self, element):
        url = self.url + '/' + self.api_key
        payload = json.dumps([element], default=lambda o: o.__dict__)
        logging.debug(payload)
        try:
            headers = {'Content-Type': 'application/json'}
            request = urllib2.Request(url, data=payload, headers=headers)
            resp = urllib2.urlopen(request)
            logging.debug("Response code: %d", resp.getcode())
            resp.close()
        except Exception as e:
            logging.exception(
                'error posting payload to api ingest endpoint (%s): %s',
                url, e)
