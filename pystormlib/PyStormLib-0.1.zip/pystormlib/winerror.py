class PyStormException(Exception):
    message = 'Oops, something bad happend'

    def __init__(self, error_code):
        message = '{}, ErrorCode: {}'.format(self.message, error_code)
        super(PyStormException, self).__init__(message)


class ErrorNoMoreFiles(PyStormException):
    message = 'No more files'


class ErrorInvalidParameter(PyStormException):
    message = 'The parameter is incorrect.'


class ErrorHandleEOF(PyStormException):
    message = 'Reached the end of the file.'


class ErrorPathNotFound(PyStormException):
    message = 'The system cannot find the path specified.'


class ErrorSharingViolation(PyStormException):
    message = 'The process cannot access the file because it is being used by another process.'


class ErrorFileNotFound(PyStormException):
    message = 'The system cannot find the file specified.'


exceptions = {
    2: ErrorFileNotFound,
    3: ErrorPathNotFound,
    18: ErrorNoMoreFiles,
    32: ErrorSharingViolation,
    87: ErrorInvalidParameter,
    38: ErrorHandleEOF
}
