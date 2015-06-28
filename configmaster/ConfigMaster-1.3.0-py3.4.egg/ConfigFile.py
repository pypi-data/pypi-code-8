import os

from configmaster import ConfigKey

class ConfigFile(object):
    """
    The abstract base class for a ConfigFile object. All config files extend from this.

    This provides several methods that don't need to be re-implemented in sub classes.
    For example, it automatically provides opening of the file and creating it if it doesn't exist, and provides a basic reload() method to automatically reload the files from disk.
    """

    def __init__(self, fd):
        self.loaded = False
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
                # Open it in write mode, then re-open it.
                open(fd, 'w').close()
                fd = open(fd, 'r')
        else:
            self.path = fd.name.replace('/', '.').replace('\\', '.')
        self.fd = fd

        self.config = None

    def dump(self):
        """
        Abstract dump method.
        """
        raise NotImplementedError

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
        self.config = ConfigKey.ConfigKey.parse_data(data)
        return True
