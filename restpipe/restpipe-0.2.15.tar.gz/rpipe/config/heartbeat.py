import os

HEARTBEAT_INTERVAL_S = int(os.environ.get('RP_CLIENT_HEARTBEAT_INTERVAL_S', '5'))
HEARTBEAT_TIMEOUT_S = int(os.environ.get('RP_CLIENT_HEARTBEAT_TIMEOUT_S', '3'))
