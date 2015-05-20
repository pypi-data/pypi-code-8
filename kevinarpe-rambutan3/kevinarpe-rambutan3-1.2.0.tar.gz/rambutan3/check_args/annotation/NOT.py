from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RLogicalNotTypeMatcher import RLogicalNotTypeMatcher


def NOT(matcher: RAbstractTypeMatcher):
    x = RLogicalNotTypeMatcher(matcher)
    return x
