from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher


RIterableMatcher = None


# noinspection PyRedeclaration
class RIterableMatcher(RAbstractTypeMatcher):
    """Iterable instance matcher

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see RArgs#is_iterable()
    """

    def __init__(self):
        # Intentional: Do not call super().__init__()
        pass

    # @override
    def matches(self, value) -> bool:
        try:
            RArgs.check_is_iterable(value, "value")
            return True
        except Exception as e:
            return False

    # @override
    def __eq__(self, other: RIterableMatcher) -> bool:
        x = isinstance(other, RIterableMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Stateless object -> Return const
        return 1

    # @override
    def __str__(self) -> str:
        return "iterable"
