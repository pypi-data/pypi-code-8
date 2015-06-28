import json
import io
from configmaster.ConfigFile import ConfigFile, NetworkedConfigObject
from configmaster import ConfigKey
from configmaster import exc

try:
    import requests
    __networked_json = True
except ImportError:
    __networked_json = False
    raise ImportWarning("Cannot use networked JSON support. Install requests to enable it.")

class JSONConfigFile(ConfigFile):
    """
    The core JSONConfigFile class.

    This handles automatically opening/creating the JSON configuration files.

    >>> import configmaster.JSONConfigFile
    >>> cfg = configmaster.JSONConfigFile.JSONConfigFile("test.json") # Accepts a string for input

    >>> fd = open("test.json") # Accepts a file descriptor too
    >>> cfg2 = configmaster.JSONConfigFile.JSONConfigFile(fd)

    ConfigMaster objects accepts either a string for the relative path of the YAML file to load, or a :io.TextIOBase: object to read from.
    If you pass in a string, the file will automatically be created if it doesn't exist. However, if you do not have permission to write to it, a :PermissionError: will be raised.

    To access config objects programmatically, a config object is exposed via the use of cfg.config.
    These config objects can be accessed via cfg.config.attr, without having to resort to looking up objects in a dict.

    >>> # Sample JSON data is {"abc": [1, 2, 3]}
    ... print(cfg.config.abc) # Prints [1, 2, 3]
    """
    def __init__(self, fd: io.TextIOBase, obj_decoder: object=None):
        """
        :param fd: The file to load.
                Either a string or a :io.TextIOBase: object.
        """
        super().__init__(fd)

        # A custom object decoder hook.
        self.decoder = obj_decoder

        self.load()

    def load(self):
        # Load the data from the JSON file.
        try:
            data = json.load(self.fd, object_hook=self.decoder)
        except ValueError as e:
            raise exc.LoaderException("Could not decode JSON file: {}".format(e))
        # Serialize the data into new sets of ConfigKey classes.
        self.config.load_from_dict(data)

    def dump(self):
        """
        Dumps all the data into a JSON file.
        """
        name = self.fd.name
        self.fd.close()
        self.fd = open(name, 'w')

        data = self.config.dump()

        json.dump(data, self.fd)
        self.reload()

    def dumps(self):
        return json.dumps(self.config.dump())


class NetworkedJSONConfigFile(NetworkedConfigObject):
    """
    This is a class for a network JSON configuration file.

    Networked JSON files are very similar to regular JSON config files, except they don't support dumping to a file.

    By default, files are verified to prevent things like

    This module requires requests to download the file.
    """
    def __init__(self, addr: str, verify=True):
        """
        :param addr: The address to load from.
        :param verify: Should we verify the data to prevent ConfigKey injection?
        """
        super().__init__(addr)
        def decode_json_object(data):
            d = {}
            # Loop over the items in the dict, to check for methods beginning with __.
            for key, value in data.items():
                if key.startswith("__") or key in ['dump', 'items', 'keys', 'values', 'iter_list', 'parse_data']:
                    # Sigh...
                    newname = 'unsafe_' + key
                else:
                    newname = key
                if isinstance(value, dict):
                    # Merge the dicts.
                    d[newname] = decode_json_object(value)
                else:
                    d[newname] = value
            return d

        self.hook = decode_json_object
        self.verify = verify

        self.load()

    def load(self):
        # Try and load file.
        if self.verify is False:
            # Use requests' JSON method.
            try:
                data = self.request.json()
            except ValueError as e:
                raise exc.LoaderException("Could not load JSON data: {}".format(e))
        else:
            # Verify the data before it comes in, to prevent overriding of our class attributes and stuff.
            try:
                data = json.loads(self.request.text, object_hook=self.hook)
            except ValueError as e:
                raise exc.LoaderException("Could not load JSON data: {}".format(e))

        # Load it into a ConfigKey.
        self.config.load_from_dict(data)

        # Done!

    def dumps(self):
        return json.dumps(self.config.dump())


if not __networked_json:
    def _(*args, **kwargs):
        raise exc.FiletypeNotSupportedException("Networked JSON support is disabled.")

    NetworkedJSONConfigFile = _
