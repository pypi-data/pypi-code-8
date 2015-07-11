"""Contains all exceptions that the application may throw"""

class RecommendyError(BaseException):
    """General recommendation error"""
    pass

class DataError(RecommendyError):
    """General data error. DataHandler classes
    are expected to throw this kind of error"""
    pass


class UnableToFetchDataError(DataError):
    """Should be thrown when a DataHandler tries to fetch
    data but for some reason is unable"""
    pass


class UnableToParseDataError(DataError):
    """Should be thrown when a DataHandler is for some reason
    unable to parse to or from a map"""
    pass


class UnableToPostDataError(DataError):
    """Should be thrown when a DataHandler tries but for some
    reason is unable to update recommendation data"""
    pass

class RecommendationError(RecommendyError):
    """General error raised when computing recommendations"""
    pass

class RecommendationDataUnavailableError(RecommendationError):
    """General error raised when for some reason fetching recommendation
    data was impossible"""
    pass
