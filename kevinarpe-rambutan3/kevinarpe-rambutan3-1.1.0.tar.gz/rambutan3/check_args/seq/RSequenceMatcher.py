from rambutan3 import RArgs
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


class RSequenceMatcher(RInstanceMatcher):

    def __init__(self, sequence_enum: RSequenceEnum):
        RArgs.check_is_instance(sequence_enum, RSequenceEnum, "sequence_enum")
        super().__init__(*(sequence_enum.value))