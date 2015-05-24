from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceMatcher import RSequenceMatcher
from rambutan3.string import RStrUtil
from rambutan3.string.RMessageText import RMessageText


class RUniqueSequenceMatcher(RSequenceMatcher):

    def __init__(self, sequence_enum: RSequenceEnum):
        super().__init__(sequence_enum)

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not super().matches(seq, matcher_error):
            return False

        x = self.core_matches(self, seq, matcher_error)
        return x

    @classmethod
    def core_matches(cls, self: RAbstractTypeMatcher, seq, matcher_error: RTypeMatcherError=None) -> bool:
        dupe_tuple_list = []
        value_set = set()
        for index, value in enumerate(seq):
            if value in value_set:
                dupe_tuple_list.append((index, value))
            else:
                value_set.add(value)

        if not dupe_tuple_list:
            return True

        if matcher_error:
            s = ', '.join(['({}: {})'.format(idx, RStrUtil.auto_quote(val)) for (idx, val) in dupe_tuple_list])
            m = 'Duplicates (index: value): ' + s
            matcher_error.add_failed_match(self, seq, RMessageText(m))

        return False

    # @override
    def __str__(self):
        x = "unique {}".format(super().__str__())
        return x
