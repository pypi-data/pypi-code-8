from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher


RNoneTypeMatcher = None


# noinspection PyRedeclaration
class RNoneTypeMatcher(RAbstractTypeMatcher):

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value) -> bool:
        x = value is None
        return x

    # @override
    def __eq__(self, other: RNoneTypeMatcher) -> bool:
        x = isinstance(other, RNoneTypeMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = super(object, self).__hash__()
        return x

    # @override
    def __str__(self):
        return "None"
