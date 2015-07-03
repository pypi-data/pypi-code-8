import configparser
from configmaster import ConfigFile
from configmaster import exc

class INIConfigFile(ConfigFile.ConfigFile):
    """
    The core INIConfigFile class.

    This handles automatically opening/creating the INI configuration files.

    >>> import configmaster.INIConfigFile
    >>> cfg = configmaster.INIConfigFile.INIConfigFile("tesr.ini") # Accepts a string for input

    >>> fd = open("test.ini") # Accepts a file descriptor too
    >>> cfg2 = configmaster.INIConfigFile.INIConfigFile(fd)

    ConfigMaster objects accepts either a string for the relative path of the INI file to load, or a :io.TextIOBase: object to read from.
    If you pass in a string, the file will automatically be created if it doesn't exist. However, if you do not have permission to write to it, a :PermissionError: will be raised.

    To access config objects programmatically, a config object is exposed via the use of cfg.config.
    These config objects can be accessed via cfg.config.attr, without having to resort to looking up objects in a dict.

    """
    def __init__(self, fd: str, safe_load: bool=True):
        """
        :param fd: The file to load.
                Either a string or a :io.TextIOBase: object.
        """
        self.tmpini = None
        super().__init__(fd, safe_load)

    def load(self):
        # Load the data from the INI file.
        self.tmpini = configparser.ConfigParser()
        try:
            self.tmpini.read_file(self.fd)
        except ValueError as e:
            raise exc.LoaderException("Could not decode INI file: {}".format(e))
        # Sanitize data.
        tmpdict = {}
        for name in self.tmpini.sections():
            data = dict(self.tmpini[name])
            tmpdict[name] = data

        # Serialize the data into new sets of ConfigKey classes.
        self.config.load_from_dict(tmpdict)

    def dump(self):
        """
        Dumps all the data into a INI file.

        This will automatically kill anything with a '_' in the keyname, replacing it with a dot. You have been warned.
        """
        name = self.fd.name
        self.fd.close()
        self.fd = open(name, 'w')

        data = self.config.dump()

        # Load data back into the goddamned ini file.
        ndict = {}
        for key, item in data.items():
            key = key.replace('_', '.')
            ndict[key] = item

        self.tmpini = configparser.ConfigParser()
        self.tmpini.read_dict(data)

        self.tmpini.write(self.fd)
        self.reload()

    def dumps(self):
        raise NotImplementedError

