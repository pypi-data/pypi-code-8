from enum import Enum


class REnum(Enum):

    def __init__(self, *args):
        """To understand why unused *args and no **kwargs, see {@link EnumMeta#__new__()}."""
        super().__init__()

    @property
    def full_name(self):
        x = self.__str__()
        return x
