from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.range.RRange_ import RRange_


RNumberRangeMatcher = None
class RNumberRangeMatcher(RAbstractTypeMatcher):

    __ALLOWED_TYPE_TUPLE = (int, float)

    def __init__(self,
                 number_matcher: RAbstractTypeMatcher,
                 bound_op1: str,
                 value1: (int, float),
                 bound_op2: str=None,
                 value2: (int, float)=None):
        super().__init__()
        RArgs.check_is_instance(number_matcher, RAbstractTypeMatcher, "matcher")
        self.__number_matcher = number_matcher
        self.__range = RRange_.create(bound_op1, value1, bound_op2, value2)

    # @override
    def matches(self, value: (int, float)) -> bool:
        if not self.__number_matcher.matches(value):
            return False
        x = (value in self.__range)
        return x

    # @override
    def __eq__(self, other: RNumberRangeMatcher) -> bool:
        if not isinstance(other, RNumberRangeMatcher):
            return False
        if not super().__eq__(other):
            return False
        x = (self.__range == other.__range)
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        super_hash = super().__hash__()
        self_hash = hash(self.__range)
        x = super_hash ^ self_hash
        return x

    # @override
    def __str__(self):
        x = "{}: {}".format(super().__str__(), self.__range)
        return x
