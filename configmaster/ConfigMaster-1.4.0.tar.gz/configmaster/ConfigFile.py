import os
try:
    import requests
    __network = True
except ImportError:
    __network = False
    raise ImportWarning("Cannot use networked config support. Install requests to enable it.")

from configmaster import ConfigKey
from configmaster import exc

class ConfigObject(object):
    """
    The abstract base class for a Config object.

    All types of config file extend from this.

    This provides several methods that don't need to be re-implemented in sub classes.
    """

    def __init__(self, safe_load: bool=True):
        self.safe_load = safe_load
        self.config = ConfigKey.ConfigKey(safe_load)

    def dumps(self) -> str:
        """
        Abstract dump to string method.
        """
        raise NotImplementedError

    def dumpd(self) -> dict:
        """
        Dump config data to a dictionary.
        """
        return self.config.dump()

    def load(self):
        """
        Abstract load method.
        """
        raise NotImplementedError

class ConfigFile(ConfigObject):
    """
    The abstract base class for a ConfigFile object. All config files extend from this.


    It automatically provides opening of the file and creating it if it doesn't exist, and provides a basic reload() method to automatically reload the files from disk.
    """
    def __init__(self, fd: str, safe_load: bool=True, json_fix: bool=False):
        super().__init__(safe_load)
        # Check if fd is a string
        if isinstance(fd, str):
            self.path = fd.replace('/', '.').replace('\\', '.')
            # Open the file.
            try:
                fd = open(fd)
            except FileNotFoundError:
                # Make sure the directory exists.
                if not os.path.exists('/'.join(fd.split('/')[:-1])) and '/' in fd:
                        os.makedirs('/'.join(fd.split('/')[:-1]))
                if not json_fix:
                    # Open it in write mode, and close it.
                    open(fd, 'w').close()
                else:
                    # Open it in write mode, write "{}" to it, and close it.
                    with open(fd, 'w') as f: f.write("{}")
                fd = open(fd, 'r')
        else:
            self.path = fd.name.replace('/', '.').replace('\\', '.')
        self.fd = fd

        self.load()
        self.fd.seek(0)

    def dump(self):
        """
        Abstract dump method.
        """
        raise NotImplementedError


    def reload(self):
        """
        Automatically reloads the config file.

        This is just an alias for self.load()."""

        if not self.fd.closed: self.fd.close()

        self.fd = open(self.fd.name, 'r')
        self.load()

    def initial_populate(self, data):
        """
        Repopulate the ConfigMaster object with data.
        :param data: The data to populate.
        :return: If it was populated.
        """
        if self.config.parsed:
            return False
        # Otherwise, create a new ConfigKey.
        self.config.load_from_dict(data)
        return True

class NetworkedConfigObject(ConfigObject):
    def __init__(self, url: str, safe_load: bool=True):
        super().__init__(safe_load=safe_load)
        self.url = url
        # Try and get url.
        try:
            self.request = requests.get(self.url)
        except requests.exceptions.ConnectionError as e:
            raise exc.NetworkedFileException("Failed to download file: {}".format(e))

        if self.request.status_code != 200:
            raise exc.NetworkedFileException("Failed to download file: Status code responded was {}".format(self.request.status_code))

    def dump(self):
        raise exc.WriterException("Cannot write to a networked JSON file.")

    def initial_populate(self, data):
        raise exc.WriterException("Cannot write to a networked JSON file.")
