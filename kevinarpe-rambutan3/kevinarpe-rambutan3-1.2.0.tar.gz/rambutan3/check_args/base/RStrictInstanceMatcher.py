from rambutan3.check_args.base.RAbstractForwardingTypeMatcher import RAbstractForwardingTypeMatcher
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher


RStrictInstanceMatcher = None


# noinspection PyRedeclaration
class RStrictInstanceMatcher(RAbstractForwardingTypeMatcher):
    """Strict type instance matcher -- subclasses do not match

    Example: Instance of Y will match type Y, but not type X.
    class X:
        pass
    class Y(X):
        pass

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see builtins#type()
    """

    def __init__(self, *class_or_type_tuple):
        """
        @param *class_or_type_tuple
               one or more value type classes, e.g., {@link str} or {@link float}

        @throws ValueError
                if {@code *class_or_type_tuple} is empty
        @throws TypeError
                if {@code *class_or_type_tuple} contains a item that is not a type/class
        """
        super().__init__()
        self.__matcher = RInstanceMatcher(*class_or_type_tuple)
        self.__class_or_type_tuple = class_or_type_tuple

    # @overrides
    @property
    def _delegate(self) -> RAbstractTypeMatcher:
        return self.__matcher

    # @overrides
    def matches(self, value) -> bool:
        value_type = type(value)
        x = any(value_type is class_or_type for class_or_type in self.__class_or_type_tuple)
        return x
