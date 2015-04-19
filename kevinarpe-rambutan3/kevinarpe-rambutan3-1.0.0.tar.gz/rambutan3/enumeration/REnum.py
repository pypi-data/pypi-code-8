from enum import Enum


class REnum(Enum):

    def __init__(self, *args):
        """To understand why unused *args and no **kwargs, see {@link EnumMeta#__new__()}."""
        super().__init__()
        self.__full_name = "{}.{}".format(type(self).__name__, self.name)

    @property
    def full_name(self):
        return self.__full_name
