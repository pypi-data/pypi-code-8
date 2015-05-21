from abc import abstractmethod
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.error.RTypeMatcherErrorFormatter import RTypeMatcherErrorFormatter


class RAbstractForwardingTypeMatcher(RAbstractTypeMatcher):

    @property
    @abstractmethod
    def _delegate(self) -> RAbstractTypeMatcher:
        """Do not forget to include decorator @property in the overriding subclasses!"""
        raise NotImplementedError()

    # @override
    def matches(self, value) -> bool:
        x = self._delegate.matches(value)
        return x

    # @override
    def check(self,
              value,
              error_formatter: RTypeMatcherErrorFormatter=RTypeMatcherErrorFormatter(),
              *args,
              **kwargs) -> None:
        self._delegate.check(value, error_formatter, *args, **kwargs)

    # @override
    def __or__(self, other: RAbstractTypeMatcher) -> RAbstractTypeMatcher:
        x = self._delegate.__or__(other)
        return x

    # @override
    def __eq__(self, other: RAbstractTypeMatcher) -> bool:
        if not isinstance(other, type(self)):
            return False
        x = self._delegate.__eq__(other._delegate)
        return x

    # @override
    def __ne__(self, other: RAbstractTypeMatcher) -> bool:
        if not isinstance(other, type(self)):
            return True
        x = self._delegate.__ne__(other._delegate)
        return x

    # @override
    def __hash__(self) -> int:
        x = self._delegate.__hash__()
        return x

    # @override
    def __str__(self) -> str:
        x = self._delegate.__str__()
        return x
