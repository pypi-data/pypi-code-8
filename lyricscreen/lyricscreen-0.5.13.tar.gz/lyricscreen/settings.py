"""

Daniel "lytedev" Flanagan
http://dmf.me

Application user settings manager.

"""

import json, os
from pprint import pprint

default_settings_file = "lyricscreen_config.json"

global settings

class Settings(dict):
    def __init__(self, file=None):
        self.defaults()
        if file == '' or file is not None:
            self.file = file
        else:
            self.file = default_settings_file
        if self.file != '':
            self.load()

    def defaults(self):
        self.cfg = {
            "websocket_port": 8417,
            "websocket_host": "127.0.0.1",
            "http_port": 8000,
            "http_host": "127.0.0.1",
            "verbose": False,
            "data_dir": "./data",
            "songs_dir": "songs",
            "playlists_dir": "playlists",
            "web_client": True,
            # TODO: Default playlist in default config?
            # TODO: Default admin password
        }

    def __getattr__(self, a):
        if a in self:
            return self[a]
        return self.cfg[a]

    def settings_json(self):
        return json.dumps(self.cfg, cls=SettingsEncoder, indent=2)

    def save(self, file=None):
        if file:
            self.file = file
        f = open(self.file, 'w+')
        if f:
            f.write(self.settings_json())
            f.close()

    def load(self, file=None):
        if file:
            self.file = file
        if os.path.isfile(self.file):
            self.cfg = json.loads(open(self.file, 'r').read(), cls=SettingsDecoder)
        else:
            if self.file == default_settings_file:
                settings = Settings('')
                settings.save(default_settings_file)
                print("Created config file at %s" % settings.file)
            else:
                print("Error: Failed to load settings file %s" % self.file)

class SettingsEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Settings):
            return super(SettingsEncoder, self).default(obj)
        return obj.cfg

class SettingsDecoder(json.JSONDecoder):
    def default(self, s):
        return super(SettingsDecoder, self).default(s)

settings = Settings()
