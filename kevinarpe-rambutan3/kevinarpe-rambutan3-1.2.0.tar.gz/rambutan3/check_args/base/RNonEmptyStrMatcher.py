from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.string.RNonEmptyStr import RNonEmptyStr

RNonEmptyStrMatcher = None


# noinspection PyRedeclaration
class RNonEmptyStrMatcher(RAbstractTypeMatcher):

    def __init__(self):
        # Intentional: Do not call super().__init__()
        pass

    # @override
    def matches(self, value) -> bool:
        if isinstance(value, RNonEmptyStr):
            return True
        if not isinstance(value, str):
            return False
        x = (0 != len(value))
        return x

    # @override
    def __eq__(self, other: RNonEmptyStrMatcher) -> bool:
        x = isinstance(other, RNonEmptyStrMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self)
        return x

    # @override
    def __str__(self) -> str:
        return "non-empty str"
