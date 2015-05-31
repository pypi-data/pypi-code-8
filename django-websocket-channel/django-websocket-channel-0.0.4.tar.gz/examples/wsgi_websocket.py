# entry point for the websocket loop
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from websocket_channel.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()
