from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RDictMatcher import RDictMatcher


RDictOfMatcher = None
class RDictOfMatcher(RDictMatcher):

    def __init__(self, dict_enum: RDictEnum, *,
                 key_matcher: RAbstractTypeMatcher=None,
                 type_matcher: RAbstractTypeMatcher=None):
        super().__init__(dict_enum)
        self.check_init_args(key_matcher=key_matcher, type_matcher=type_matcher)
        self.__key_matcher = key_matcher
        self.__type_matcher = type_matcher

    # @override
    def matches(self, d: dict) -> bool:
        if not super().matches(d):
            return False
        x = self.core_matches(d, key_matcher=self.__key_matcher, type_matcher=self.__type_matcher)
        return x

    # @override
    def __eq__(self, other: RDictOfMatcher) -> bool:
        if not isinstance(other, RDictOfMatcher):
            return False
        if not super().__eq__(other):
            return False
        x = (self.__key_matcher == other.__key_matcher and self.__type_matcher == other.__type_matcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        super_hash = super().__hash__()
        self_hash = hash((self.__key_matcher, self.__type_matcher))
        x = super_hash ^ self_hash
        return x

    # @override
    def __str__(self):
        x = self.core__str__(super().__str__(), key_matcher=self.__key_matcher, type_matcher=self.__type_matcher)
        return x

    @classmethod
    def check_init_args(cls, *,
                        key_matcher: RAbstractTypeMatcher=None,
                        type_matcher: RAbstractTypeMatcher=None):
        if key_matcher is None and type_matcher is None:
            raise ValueError("Both args 'key_matcher' and 'type_matcher' are None")

        if key_matcher is not None:
            RArgs.check_is_instance(key_matcher, RAbstractTypeMatcher, "key_matcher")

        if type_matcher is not None:
            RArgs.check_is_instance(type_matcher, RAbstractTypeMatcher, "type_matcher")

    @classmethod
    def core_matches(cls, dictionary: dict, *,
                     key_matcher: RAbstractTypeMatcher=None,
                     type_matcher: RAbstractTypeMatcher=None):
        if key_matcher:
            for key in dictionary.keys():
                if not key_matcher.matches(key):
                    return False

        if type_matcher:
            for value in dictionary.values():
                if not type_matcher.matches(value):
                    return False

        return True

    @classmethod
    def core__str__(cls, super_str: str, *,
                 key_matcher: RAbstractTypeMatcher=None,
                 type_matcher: RAbstractTypeMatcher=None):
        m = ""

        if key_matcher:
            m = "keys: {}".format(key_matcher)

        if type_matcher:
            if m:
                m += ", "
            m += "values: {}".format(type_matcher)

        x = "{} of [{}]".format(super_str, m)
        return x
