from __future__ import absolute_import

import schematec.converters
import schematec.validators


class Schema(object):
    '''
    Converters is appliyed first in orderder they defined
    Validators is appliyed second.
    '''

    def __init__(self, **descriptors):
        self.descriptors = descriptors

    def __call__(self, data):
        result = {}
        for name, descriptors in self.descriptors.items():
            unbound_validators = [v for v in descriptors if
                                  isinstance(v, schematec.validators.Validator) and not v.BINDING]
            for validator in unbound_validators:
                validator(name, data)
            try:
                value = data[name]
            except KeyError:
                continue
            converters = [c for c in descriptors if isinstance(c, schematec.converters.Converter)]
            for converter in converters:
                value = converter(value)
            bound_validators = [v for v in descriptors if isinstance(v, schematec.validators.Validator) and v.BINDING]
            for validator in bound_validators:
                if isinstance(value, validator.BINDING):
                    validator(value)
            result[name] = value
        return result
