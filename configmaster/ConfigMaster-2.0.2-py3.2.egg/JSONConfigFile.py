import json

from configmaster.ConfigFile import ConfigFile, NetworkedConfigObject
from configmaster import exc

from .ConfigGenerator import GenerateConfigFile, GenerateNetworkedConfigFile

try:
    import requests

    __networked_json = True
except ImportError:
    __networked_json = False
    raise ImportWarning("Cannot use networked JSON support. Install requests to enable it.")

def json_load_hook(is_net: bool=False):
    def actual_load_hook(cfg):
        """
        This handles automatically opening/creating the JSON configuration files.

        >>> import configmaster.JSONConfigFile
        >>> cfg = configmaster.JSONConfigFile.JSONConfigFile("test.json") # Accepts a string for input

        >>> fd = open("test.json") # Accepts a file descriptor too
        >>> cfg2 = configmaster.JSONConfigFile.JSONConfigFile(fd)

        ConfigMaster objects accepts either a string for the relative path of the INI file to load, or a :io.TextIOBase: object to read from.
        If you pass in a string, the file will automatically be created if it doesn't exist. However, if you do not have permission to write to it, a :PermissionError: will be raised.

        To access config objects programmatically, a config object is exposed via the use of cfg.config.
        These config objects can be accessed via cfg.config.attr, without having to resort to looking up objects in a dict.

        >>> # Sample JSON data is {"abc": [1, 2, 3]}
        ... print(cfg.config.abc) # Prints [1, 2, 3]
        """
        # Load the data from the JSON file.
        try:
            if not is_net:
                data = json.load(cfg.fd)
            else:
                data = json.load(cfg.request.text)
        except ValueError as e:
            raise exc.LoaderException("Could not decode JSON file: {}".format(e))
        # Serialize the data into new sets of ConfigKey classes.
        print(data)
        cfg.config.load_from_dict(data)

    return actual_load_hook

def json_dump_hook(cfg):
    """
    Dumps all the data into a JSON file.
    """
    name = cfg.fd.name
    cfg.fd.close()
    cfg.fd = open(name, 'w')

    data = cfg.config.dump()

    json.dump(data, cfg.fd)
    cfg.reload()


JSONConfigFile = GenerateConfigFile(load_hook=json_load_hook(False), dump_hook=json_dump_hook, json_fix=True)
NetworkedJSONConfigFile = GenerateNetworkedConfigFile(load_hook=json_load_hook(True),
                        normal_class_load_hook=json_load_hook(False), normal_class_dump_hook=json_dump_hook)

if not __networked_json:
    def _(*args, **kwargs):
        raise exc.FiletypeNotSupportedException("Networked JSON support is disabled.")

    NetworkedJSONConfigFile = _
