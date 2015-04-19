from rambutan3.enumeration.REnum import REnum
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER


class RTypedEnum(REnum):

    @check_args
    def __init__(self: SELF(), type_matcher: TYPE_MATCHER):
        """Argument {@code type_matcher} is unused in this ctor (except for validation via
        {@link RCheckArgs#check_args}), but automagically assigned to property {@link Enum#value}.
        """
        super().__init__()
