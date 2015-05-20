from rambutan3 import RTypes
from rambutan3.check_args.other.RRegexMatcher import RRegexMatcher


def STR_MATCHES_REGEX(regex_pattern: RTypes.REGEX_PATTERN_TYPE) -> RRegexMatcher:
    x = RRegexMatcher(regex_pattern)
    return x
