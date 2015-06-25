import json
import io
from configmaster.ConfigFile import ConfigFile
from configmaster import ConfigKey
from configmaster import exc


class JSONConfigFile(ConfigFile):
    """
    The core JSONConfigFile class.

    This handles automatically opening/creating the JSON configuration files.

    >>> import configmaster.JSONConfigFile
    >>> cfg = configmaster.JSONConfigFile.JSONConfigFile("test.yml") # Accepts a string for input

    >>> fd = open("test.yml") # Accepts a file descriptor too
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
        self.config = None

        # A custom object decoder hook.
        self.decoder = obj_decoder

        self.load()


    def load(self):
        # Load the data from the JSON file.
        try:
            data = json.load(self.fd, object_hook=self.decoder)
        except json.JSONDecodeError as e:
            raise exc.LoaderException("Could not decode JSON file: {}".format(e))
        # Serialize the data into new sets of ConfigKey classes.
        self.config = ConfigKey.ConfigKey.parse_data(data)


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

    def initial_populate(self, data):
        """
        Repopulate the ConfigMaster object with data.
        :param data: The data to populate.
        :return: If it was populated.
        """
        if self.config.parsed:
            return False
        # Otherwise, create a new ConfigKey.
        self.config = ConfigKey.ConfigKey.parse_data(data)
        return True
