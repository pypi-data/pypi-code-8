"""
Controller to interface with the Plex-app.
"""
from . import BaseController

MESSAGE_TYPE = 'type'

TYPE_PLAY = "PLAY"
TYPE_PAUSE = "PAUSE"
TYPE_STOP = "STOP"

CONTENT_TYPE_VIDEO = "video"


class PlexController(BaseController):
    """ Controller to interact with Plex namespace. """

    def __init__(self):
        super(PlexController, self).__init__(
            "urn:x-cast:plex", "9AC194DC")

    def stop(self):
        """ Send stop command. """
        self.send_message({MESSAGE_TYPE: TYPE_STOP})

    def pause(self):
        """ Send pause command. """
        self.send_message({MESSAGE_TYPE: TYPE_PAUSE})

    def play(self):
        """ Send play command. """
        self.send_message({MESSAGE_TYPE: TYPE_PLAY})

    def play_media(self, content_id, content_type):
        """ media namespace
        {'autoplay': True,
         'currentTime': 1494.541,
         'media': {'contentId': '/library/metadata/47529',
                   'contentType': 'video',
                   'customData': {
                      'audioBoost': 100,
                      'bitrate': '8000',
                      'containerKey': '/playQueues/116?own=1&window=200',
                      'directPlay': True,
                      'directStream': True,
                      'offset': 1494.541,
                      'quality': '60',
                      'resolution': '1920x1080',
                      'server': {'accessToken': 'sy2f9ekocgNhqHhAZVsy',
                                 'address': '192.168.1.150',
                                 'machineIdentifier':
                                  'aeb78eed8f59bc301816aa802f9fb9068f9297d6',
                                 'port': 32400,
                                 'transcoderAudio': True,
                                 'transcoderVideo': True,
                                 'version': '0.9.10.3'},
                      'subtitleSize': 100,
                      'user': {'username': 'balloob'}},
                   'streamType': 'BUFFERED'},
         'requestId': 93233066,
         'sessionId': '2FCCB176-AAB6-ABF7-32F2-5D7B14AAF27D',
         'type': 'LOAD'}
         """
