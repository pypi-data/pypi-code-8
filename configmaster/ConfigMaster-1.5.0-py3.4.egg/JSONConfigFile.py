import json

from configmaster.ConfigFile import ConfigFile, NetworkedConfigObject
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

    ConfigMaster objects accepts either a string for the relative path of the INI file to load, or a :io.TextIOBase: object to read from.
    If you pass in a string, the file will automatically be created if it doesn't exist. However, if you do not have permission to write to it, a :PermissionError: will be raised.

    To access config objects programmatically, a config object is exposed via the use of cfg.config.
    These config objects can be accessed via cfg.config.attr, without having to resort to looking up objects in a dict.

    >>> # Sample JSON data is {"abc": [1, 2, 3]}
    ... print(cfg.config.abc) # Prints [1, 2, 3]
    """

    def __init__(self, fd: str, safe_load: bool=True, obj_decoder: object=None):
        """
        :param fd: The file to load.
                Either a string or a :io.TextIOBase: object.
        """
        # A custom object decoder hook.
        self.decoder = obj_decoder
        super().__init__(fd, safe_load, json_fix=True)
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

    def __init__(self, addr: str, custom_object_hook=None):
        """
        :param addr: The address to load from.
        :param custom_object_hook: The object hook to use, if specified.
        """
        self.object_hook = custom_object_hook
        super().__init__(addr)

        self.load()

    def load(self):
        # Try and load file.
        if self.object_hook is None:
            # Use requests' JSON method.
            try:
                data = self.request.json()
            except ValueError as e:
                raise exc.LoaderException("Could not load JSON data: {}".format(e))
        else:
            # Use a custom object hook.
            try:
                data = json.loads(self.request.text, object_hook=self.object_hook)
            except ValueError as e:
                raise exc.LoaderException("Could not load JSON data: {}".format(e))

        # Load it into a ConfigKey.
        self.config.load_from_dict(data)

        # Done!

    def dumps(self):
        return json.dumps(self.config.dump())

    def __create_normal_class(self, filename: str):
        return JSONConfigFile(fd=filename, safe_load=self.safe_load)


if not __networked_json:
    def _(*args, **kwargs):
        raise exc.FiletypeNotSupportedException("Networked JSON support is disabled.")

    NetworkedJSONConfigFile = _
