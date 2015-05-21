# -*- test-case-name: mimic.test.test_auth -*-
"""
API Mock for Mail Gun.
https://documentation.mailgun.com/api-sending.html
"""

import json
from random import randrange

from mimic.rest.mimicapp import MimicApp
items = {}


class MailGunApi(object):
    """
    Rest endpoints for mocked Mail Gun api.
    """

    app = MimicApp()

    def __init__(self, core, clock):
        """
        :param MimicCore core: The core to which this Mail Gun Api will be
        communicating.
        """
        self.core = core
        self.clock = clock

    @app.route('/messages', methods=['POST'])
    def send_messages(self, request):
        """
        Responds with a 200 with a static response.
        """
        content = str(request.content.read())
        print self.clock.seconds()
        # message_id =
        request.setResponseCode(200)
        items.update({'message_id': content})
        return json.dumps({
            "message": "Queued. Thank you.",
            "id": "<20120315083536.28675.36480@samples.mailgun.org>"})

    @app.route('/messages', methods=['GET'])
    def get_message_count(self, request):
        """
        Responds with a 200 and the number of messages POSTed
        through the ``/messages`` endpoint.
        """
        request.setResponseCode(200)
        return json.dumps({"message_count": len(items)})
