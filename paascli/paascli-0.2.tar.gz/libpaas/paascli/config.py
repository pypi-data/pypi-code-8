__author__ = 'hvishwanath'

import os
from libpaas import settings

class Config(object):
    __singleton = None # the one, true Singleton

    def __new__(cls, *args, **kwargs):
        # Check to see if a __singleton exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __singleton objects
        if cls != type(cls.__singleton):
        #if not cls.__singleton:
            cls.__singleton = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    @classmethod
    def getInstance(cls, *args):
        '''
        Returns a singleton instance of the class
        '''
        if not cls.__singleton:
            cls.__singleton = Config(*args)
        return cls.__singleton

    @classmethod
    def read_yaml_file(cls, file_name):
        import yaml
        parsed_yaml = None
        if os.path.isfile(file_name):
            with open(file_name, 'r') as fp:
                parsed_yaml = yaml.safe_load(fp)

        return parsed_yaml

    @classmethod
    def write_yaml_file(cls, file_name, data, def_flow_style=False):
        import yaml
        with open(file_name, 'w') as fp:
            fp.write(yaml.dump(data, default_flow_style=def_flow_style))


    def __init__(self):
        self.cfgfile = settings.cfgfile
        if not os.path.isfile(self.cfgfile):
            file(self.cfgfile, "w").write("# config file\n")

    def reset(self):
        if os.path.isfile(self.cfgfile):
            os.remove(self.cfgfile)