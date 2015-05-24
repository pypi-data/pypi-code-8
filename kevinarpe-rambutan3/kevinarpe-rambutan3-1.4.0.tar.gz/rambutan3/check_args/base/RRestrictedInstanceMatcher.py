from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractForwardingTypeMatcher import RAbstractForwardingTypeMatcher
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError

RRestrictedInstanceMatcher = None


# noinspection PyRedeclaration
class RRestrictedInstanceMatcher(RAbstractForwardingTypeMatcher):
    """Restricted type instance matcher -- certain subclasses may be excluded.
    This class primarily exists to restrict bools from matching ints, as bool is a subclass of int.

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see builtins#type()
    """

    # noinspection PyMissingConstructor
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
        # Intentional: Do not call super(RAbstractForwardingTypeMatcher, self).__init__()
        RArgs.check_is_instance(allowed_class_or_type_tuple, tuple, "allowed_class_or_type_tuple")
        RArgs.check_is_instance(not_allowed_class_or_type_tuple, tuple, "not_allowed_class_or_type_tuple")
        self.__matcher = RInstanceMatcher(*allowed_class_or_type_tuple)
        self.__not_allowed_class_or_type_tuple = not_allowed_class_or_type_tuple

    # @overrides
    @property
    def _delegate(self) -> RAbstractTypeMatcher:
        return self.__matcher

    # @overrides
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__matcher.matches(value, matcher_error):
            return False

        x = not isinstance(value, self.__not_allowed_class_or_type_tuple)

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x
