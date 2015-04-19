from rambutan3 import RArgs
from rambutan3.check_args.collection.RRangeSizeCollectionMatcher import RRangeSizeCollectionMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


class RRangeSizeSequenceMatcher(RRangeSizeCollectionMatcher):

    def __init__(self, sequence_enum: RSequenceEnum, *, min_size: int=-1, max_size: int=-1):
        RArgs.check_is_instance(sequence_enum, RSequenceEnum, "sequence_enum")
        super().__init__(sequence_enum.value, min_size=min_size, max_size=max_size)
