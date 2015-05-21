from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.iter.RNonEmptyIterableOfMatcher import RNonEmptyIterableOfMatcher


def NON_EMPTY_ITERABLE_OF(type_matcher: RAbstractTypeMatcher):
        x = RNonEmptyIterableOfMatcher(type_matcher)
        return x
