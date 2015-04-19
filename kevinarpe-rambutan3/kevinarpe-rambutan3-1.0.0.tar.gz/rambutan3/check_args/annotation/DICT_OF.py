from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RDictOfMatcher import RDictOfMatcher


def DICT_OF(*,
            key_matcher: RAbstractTypeMatcher=None,
            type_matcher: RAbstractTypeMatcher=None) \
        -> RDictOfMatcher:
    x = RDictOfMatcher(RDictEnum.DICT, key_matcher=key_matcher, type_matcher=type_matcher)
    return x
