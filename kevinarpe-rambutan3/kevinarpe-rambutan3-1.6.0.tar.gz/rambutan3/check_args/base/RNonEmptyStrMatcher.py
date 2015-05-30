from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.string.RNonEmptyStr import RNonEmptyStr


class RNonEmptyStrMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        pass

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        if isinstance(value, RNonEmptyStr):
            return True

        if isinstance(value, str):
            x = (0 != len(value))
        else:
            x = False

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __eq__(self, other) -> bool:
        x = isinstance(other, RNonEmptyStrMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = super(object, self).__hash__()
        return x

    # @override
    def __str__(self) -> str:
        return "non-empty str"
