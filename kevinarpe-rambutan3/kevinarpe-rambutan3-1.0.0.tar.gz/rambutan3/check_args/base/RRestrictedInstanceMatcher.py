from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractForwardingTypeMatcher import RAbstractForwardingTypeMatcher
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher


RRestrictedInstanceMatcher = None
class RRestrictedInstanceMatcher(RAbstractForwardingTypeMatcher):
    """Restricted type instance matcher -- certain subclasses may be excluded.
    This class primarily exists to restrict bools from matching ints, as bool is a subclass of int.

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see builtins#type()
    """

    def __init__(self, *,
                 allowed_class_or_type_tuple: tuple,
                 not_allowed_class_or_type_tuple: tuple):
        """
        @param allowed_class_or_type_tuple
               tuple of allowed value type classes, e.g., {@link int}
        @param not_allowed_class_or_type_tuple
               tuple of not allowed value type classes, e.g., {@link bool}

        @throws ValueError
                if {@code allowed_class_or_type_tuple} is empty
        @throws TypeError
                if {@code allowed_class_or_type_tuple} contains a item that is not a type/class
        """
        super().__init__()
        RArgs.check_is_instance(allowed_class_or_type_tuple, tuple, "allowed_class_or_type_tuple")
        RArgs.check_is_instance(not_allowed_class_or_type_tuple, tuple, "not_allowed_class_or_type_tuple")
        self.__matcher = RInstanceMatcher(*allowed_class_or_type_tuple)
        self.__not_allowed_class_or_type_tuple = not_allowed_class_or_type_tuple

    # @overrides
    @property
    def _delegate(self) -> RAbstractTypeMatcher:
        return self.__matcher

    # @overrides
    def matches(self, value) -> bool:
        if not super().matches(value):
            return False
        x = not isinstance(value, self.__not_allowed_class_or_type_tuple)
        return x
