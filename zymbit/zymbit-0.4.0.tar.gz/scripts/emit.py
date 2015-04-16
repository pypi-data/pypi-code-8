import datetime
import json
import logging
import sys
import uuid

from zymbit.client import Client


def timestamp():
    return datetime.datetime.utcnow().isoformat('T')


def main(client_id, device_id, value):
    client = Client()

    envelope = json.dumps({
        'message_id': str(uuid.uuid4()),
        'client_id': client_id,
        'timestamp': timestamp(),
        'action': 'store',
        'message': [
            {'deviceId': device_id, 'timestamp': timestamp(), 'value': value},
        ],
    })

    client.ws.send(envelope)
    client.ws.close()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    client_id = sys.argv[1]
    device_id = str(sys.argv[2])
    value = float(sys.argv[3])

    main(client_id, device_id, value)
