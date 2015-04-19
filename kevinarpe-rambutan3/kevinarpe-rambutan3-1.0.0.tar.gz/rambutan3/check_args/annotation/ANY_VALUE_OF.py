from rambutan3.check_args.base.RAnyValueOfMatcher import RAnyValueOfMatcher


def ANY_VALUE_OF(*value_tuple) -> RAnyValueOfMatcher:
    x = RAnyValueOfMatcher(*value_tuple)
    return x
