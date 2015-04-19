from functools import lru_cache
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher


@lru_cache(maxsize=None)
def INSTANCE_OF(class_or_type: type) -> RInstanceMatcher:
    x = RInstanceMatcher(class_or_type)
    return x