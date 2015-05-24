from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RUniqueSequenceMatcher import RUniqueSequenceMatcher


class RRangeSizeUniqueSequenceMatcher(RRangeSizeSequenceMatcher):

    def __init__(self, sequence_enum: RSequenceEnum, *, min_size: int=-1, max_size: int=-1):
        super().__init__(sequence_enum, min_size=min_size, max_size=max_size)

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not super().matches(seq, matcher_error):
            return False

        x = RUniqueSequenceMatcher.core_matches(self, seq, matcher_error)
        return x

    # @override
    def __str__(self):
        x = "unique {}".format(super().__str__())
        return x
