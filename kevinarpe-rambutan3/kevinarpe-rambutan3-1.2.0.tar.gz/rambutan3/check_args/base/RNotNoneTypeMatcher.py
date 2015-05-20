from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher


RNotNoneTypeMatcher = None


# noinspection PyRedeclaration
class RNotNoneTypeMatcher(RAbstractTypeMatcher):

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value) -> bool:
        x = value is not None
        return x

    # @override
    def __eq__(self, other: RNotNoneTypeMatcher) -> bool:
        x = isinstance(other, RNotNoneTypeMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = super(object, self).__hash__()
        return x

    # @override
    def __str__(self):
        return "not None"
