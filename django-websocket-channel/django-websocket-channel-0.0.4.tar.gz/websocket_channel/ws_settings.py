from django.conf import settings

WS_SETTINGS = {
    "WEBSOCKET_URL": getattr(settings, 'WEBSOCKET_URL', '/ws/'),
    "CHANNEL_MIDDLEWARE": getattr(settings, 'CHANNEL_MIDDLEWARE', 'websocket_channel.middleware.ChannelMiddleware'),
    "OTHER_REQUET": getattr(settings, 'OTHER_REQUET', None),
    "WS_REDIS": getattr(settings, 'WS_CONNECTION', {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': 'foobared',
    }),
}

