from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher


RLogicalNotTypeMatcher = None


class RLogicalNotTypeMatcher(RAbstractTypeMatcher):

    def __init__(self, delegate: RAbstractTypeMatcher):
        RArgs.check_is_instance(delegate, RAbstractTypeMatcher, "delegate")
        self.__delegate = delegate

    # @override
    def matches(self, value) -> bool:
        x = self.__delegate.matches(value)
        y = not x
        return y

    # @override
    def __eq__(self, other: RLogicalNotTypeMatcher) -> bool:
        if not isinstance(other, RLogicalNotTypeMatcher):
            return False
        x = (self.__delegate == other.__delegate)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__delegate)
        return x

    # @override
    def __str__(self):
        x = "not ".format(self.__delegate)
        return x
