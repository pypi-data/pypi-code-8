from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceOfMatcher import RSequenceOfMatcher


def SEQUENCE_OF(type_matcher: RAbstractTypeMatcher) -> RSequenceOfMatcher:
    x = RSequenceOfMatcher(RSequenceEnum.SEQUENCE, type_matcher)
    return x