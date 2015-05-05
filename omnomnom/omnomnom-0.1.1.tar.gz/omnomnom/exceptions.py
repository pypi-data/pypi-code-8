class OmnomnomException(Exception):
    """
    Base Omnomnom Exception Class.
    """


class PipConnectionException(OmnomnomException):
    """
    Raised when nanomsg cannot handle socket communication.
    """


class MarshallingException(OmnomnomException):
    """
    Raised during marshalling process.
    """


class DemarshallingExeption(OmnomnomException):
    """
    Raised during demarshalling process.
    """


class MicroServiceInitializationException(OmnomnomException):
    """
    Raised when service cannot be properly initialized
    based on its configuration.
    """


class MicroServiceRegistrationException(OmnomnomException):
    """
    Raised when executable cannot be registered.
    """


class MicroServiceExecutionException(OmnomnomException):
    """
    Raised when executable cannot be executed.
    or is not registered.
    """


class MicroServiceRunnerException(OmnomnomException):
    """
    Raised when service cannot be imported.
    """