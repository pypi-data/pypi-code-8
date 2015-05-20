from rambutan3 import RArgs
from rambutan3 import RTypes
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher

RRegexMatcher = None


# noinspection PyRedeclaration
class RRegexMatcher(RAbstractTypeMatcher):

    def __init__(self, regex_pattern: RTypes.REGEX_PATTERN_TYPE):
        # Intentional: Do not call super().__init__()
        RArgs.check_is_instance(regex_pattern, RTypes.REGEX_PATTERN_TYPE, "pattern")
        self.__regex_pattern = regex_pattern

    # @override
    def matches(self, value) -> bool:
        if not isinstance(value, str):
            return False
        x = self.__regex_pattern.search(value)
        return x

    # @override
    def __eq__(self, other: RRegexMatcher) -> bool:
        if not isinstance(other, RRegexMatcher):
            return False
        x = (self.__regex_pattern == other.__regex_pattern)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__regex_pattern)
        return x

    # @override
    def __str__(self):
        x = "str matching regex {}".format(self.__regex_pattern.pattern)
        return x
