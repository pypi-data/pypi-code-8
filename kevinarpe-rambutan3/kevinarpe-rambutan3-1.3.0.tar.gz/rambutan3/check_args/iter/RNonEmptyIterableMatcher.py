from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher


RNonEmptyIterableMatcher = None


# noinspection PyRedeclaration
class RNonEmptyIterableMatcher(RAbstractTypeMatcher):
    """Non-empty iterable instance matcher

    TOOD: This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see RArgs#check_iterable_not_empty()
    """

    def __init__(self):
        # Intentional: Do not call super().__init__()
        pass

    # @override
    def matches(self, value) -> bool:
        try:
            RArgs.check_iterable_not_empty(value, "value")
            return True
        except Exception as e:
            return False

    # @override
    def __eq__(self, other: RNonEmptyIterableMatcher) -> bool:
        x = isinstance(other, RNonEmptyIterableMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Stateless object -> Return const
        return 1

    # @override
    def __str__(self) -> str:
        return "non-empty iterable"
