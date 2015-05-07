from .validators import chained_validator


class Field(object):

    def __init__(self, validator=None, required=True,
                 validator_requires_other_fields=False):
        self.validator = validator
        self.required = required
        self.validator_requires_other_fields = validator_requires_other_fields


class MetaSchema(type):

    def __init__(self, name, bases, attrs):
        self.schema_validators = []
        super(MetaSchema, self).__init__(name, bases, attrs)
        for attrkey, attr in attrs.items():
            if hasattr(attr, 'is_schema_validator'):
                self.schema_validators.append(attr)


class Schema(object):

    __metaclass__ = MetaSchema

    schema_validators = []

    @classmethod
    def validate(cls, data):
        is_valid = True
        errors = None
        for validator in cls.schema_validators:
            schema_is_valid, schema_errors = validator(data)
            is_valid = is_valid and schema_is_valid
            if not schema_is_valid:
                if errors is None:
                    errors = {}
                errors[validator.__name__] = schema_errors
        for k, field in cls.__dict__.items():
            if isinstance(field, Field):
                if k not in data:
                    if field.required:
                        is_valid = False
                        if errors is None:
                            errors = {}
                        errors[k] = 'MissingKey'
                else:
                    if field.validator is None:
                        is_valid = is_valid & True
                    else:
                        if field.validator_requires_other_fields:
                            field_is_valid, field_errors = field.validator(
                                data)
                        else:
                            field_is_valid, field_errors = field.validator(
                                data[k])
                        is_valid = is_valid & field_is_valid
                        if not field_is_valid:
                            if errors is None:
                                errors = {}
                            errors[k] = field_errors
        return (is_valid, errors)

    @classmethod
    def validate_list(cls, datalist):
        results = [cls.validate(data) for data in datalist]
        return (all(result[0] for result in results),
                [result[1] for result in results])

    @classmethod
    def validator(cls, func):
        cls.schema_validators.append(func)
        return func


def validator(field):
    def field_validator_func_wrapper(func):
        field.validator = chained_validator(field.validator, func)
        return func
    return field_validator_func_wrapper


def schema_validator(func):
    func.is_schema_validator = True
    return func
