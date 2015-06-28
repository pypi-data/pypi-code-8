import copy


class ConfigKey(object):
    """
    A ConfigKey object is a collection that is stored via class attributes.

    >>> d = {"a": 2, "b": [1, 2, {"c": 3}], {"d": 4}}
    >>> config = ConfigKey.parse_data(d)
    >>> config.a # Returns 2
    >>> config.b[1] # Returns 2
    >>> config.b[3] # Returns a new ConfigKey, as it's a dict.

    ConfigKeys take in data from dicts, and set attributes of themselves to accommodate the items inside the dictionaries.
    There are special cases for handling lists, and all objects inside a list are automatically parsed appropriately, with dicts turning into ConfigKeys.
    """
    def __init__(self):
        self.parsed = False

    def __iter__(self):
        ndict = copy.copy(self.__dict__)
        ndict.pop('parsed')
        return ndict.__iter__()

    def __contains__(self, item):
        # Sigh.
        return item in self.__dict__

    def dump(self) -> dict:
        """
        Dumps data from the ConfigKey into a dict.
        :return: The keys and values from the ConfigKey encapsulated in a dict.
        """
        d = {}
        for item in self.__dict__:
            if item in ['parsed', 'dump', 'parse_data', 'iter_list']:
                continue
            if isinstance(self.__dict__[item], ConfigKey):
                d[item] = self.__dict__[item].dump()
            elif isinstance(self.__dict__[item], list):
                d[item] = self.iter_list_dump(self.__dict__[item])
            else:
                d[item] = self.__dict__[item]
        return d


    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def load_from_dict(self, data: dict):
        if data is None:
            return False
        for key, item in data.items():
            if isinstance(item, dict):
                # Create a new ConfigKey object with the dict.
                ncfg = ConfigKey()
                # Parse the data.
                ncfg.load_from_dict(item)
                # Set our new ConfigKey as an attribute of ourselves.
                setattr(self, key, ncfg)
            elif isinstance(item, list):
                # Iterate over the list, creating ConfigKey items as appropriate.
                nlst = self.iter_list(item)
                # Set our new list as an attribute of ourselves.
                setattr(self, key, nlst)
            else:
                # Set the item as an attribute of ourselves.
                setattr(self, key, item)
        # Flip the parsed flag,
        self.parsed = True

    def iter_list(self, data: list):
        l = []
        for item in data:
            if isinstance(item, list):
                l.append(self.iter_list(item))
            elif isinstance(item, dict):
                ncfg = ConfigKey()
                ncfg.load_from_dict(item)
                l.append(ncfg)
            else:
                l.append(item)
        return l

    def iter_list_dump(self, data: list):
        l = []
        for item in data:
            if isinstance(item, list):
                l.append(self.iter_list_dump(item))
            elif isinstance(item, ConfigKey):
                l.append(item.dump())
            else:
                l.append(item)
        return l

    @classmethod
    def parse_data(cls, data: dict):
        """
        Create a Config Key entity.
        :param data: The dict to create the entity from.
        :return: A new ConfigKey object.
        """
        cfg = ConfigKey()
        if data is None:
            return cfg
        for key, item in data.items():
            if isinstance(item, dict):
                # Create a new ConfigKey object with the dict.
                ncfg = ConfigKey.parse_data(item)
                # Set our new ConfigKey as an attribute of ourselves.
                setattr(cfg, key, ncfg)
            elif isinstance(item, list):
                # Iterate over the list, creating ConfigKey items as appropriate.
                nlst = ConfigKey.iter_list(item)
                # Set our new list as an attribute of ourselves.
                setattr(cfg, key, nlst)
            else:
                # Set the item as an attribute of ourselves.
                setattr(cfg, key, item)
        # Flip the parsed flag,
        cfg.parsed = True
        return cfg

