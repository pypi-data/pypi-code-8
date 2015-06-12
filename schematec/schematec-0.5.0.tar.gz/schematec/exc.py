class SchematecError(Exception):
    pass


class ConvertationError(SchematecError):
    pass


class ValidationError(SchematecError):
    pass


class SchemaError(SchematecError):
    pass
