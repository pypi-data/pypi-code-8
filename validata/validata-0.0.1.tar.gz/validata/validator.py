# -*- coding: utf-8 -*-

from mongoengine.document import Document
from mongoengine.errors   import ValidationError
from etl_utils            import JsonUtils


__all__ = ['Validator']

class Result(object):

    def __init__(self, data):
        self.data    = data
        self.success = False
        self.errors  = dict()

    def json(self):
        """ convert ValidationError to str type. """
        error_dict = dict()
        for k1, v1 in self.errors.iteritems():
            error_dict[k1] = str(v1)
        return {"data": self.data, "success": self.success, "errors": error_dict}

    def __str__(self): return JsonUtils.unicode_dump(self.json()).encode("UTF-8")
    __repr__ = __str__




class Validator(Document):

    @classmethod
    def do(cls, json1):
        result    = Result(json1)
        item1     = dict()
        fields    = dict(cls._fields); del fields['id']

        for field_name2, field_type2 in fields.iteritems():
            # 1. when value is None
            value2 = json1.get(field_name2, None)
            if value2 is None:
                if field_type2.required:
                    result.errors[field_name2] = ValidationError('Field is required',)
                continue
            # 2. when value exists
            else:
                # 2.1. check data type
                try:
                    value2 = field_type2.to_python(value2)
                except Exception, error:
                    result.errors[field_name2] = error

                # 2.2. check bussiness logic
                try:
                    field_type2._validate(value2)
                except ValidationError, error:
                    result.errors[field_name2] = error.errors or error
                except (ValueError, AttributeError, AssertionError), error:
                    result.errors[field_name2] = error


        if not result.errors: result.success = True


        return result


    meta = {
            'abstract': True,
           }
