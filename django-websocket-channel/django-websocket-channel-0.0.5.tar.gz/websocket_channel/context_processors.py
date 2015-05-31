# -*- coding: utf-8 -*-
from websocket_channel import ws_settings


def default(request):
    protocol = request.is_secure() and 'wss://' or 'ws://'
    context = {
        'WEBSOCKET_URL': protocol + request.get_host()+ws_settings.WS_SETTINGS['WEBSOCKET_URL'],
    }
    return context