'''
Current Side Developments
=========================

WTForms
-------
::

   class MyForm(Form):
       name    = StringField(u'Full Name', [validators.required(), validators.length(max=10)])
       address = TextAreaField(u'Mailing Address', [validators.optional(), validators.length(max=200)])

WTForms uses lists of validators. That approach helps to separate validators
from converters. `Source code <https://github.com/wtforms/wtforms/blob/master/wtforms/validators.py>`_.

::

   def __init__(self, fieldname, message=None):
       self.fieldname = fieldname
       self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)

Validators are simple objects. ``__init__`` method provides a way to configure validator.
``__call__`` method provides a way to process validation.

Validation is bound to forms objects. This has been made to provide ``EqualTo``
functionality. Reflects connections between form fields.

WTForms users ``ValidationError`` and ``StopValidation`` exceptions.
``ValidationError`` is used for errors forwarding.
``StopValidation`` is used to skip steps. Thus some validation steps could be optional.


scheme
------

Scheme `provides <https://github.com/arterial-io/scheme/tree/master/scheme/fields>`_
wide range of different types validators. It extracts types conversion into
serializers/deserializers.

django-data-schema
------------------

Module `implements <https://github.com/ambitioninc/django-data-schema/blob/develop/data_schema/convert_value.py>`_
data converters.

'''
from .converters import (
    integer,
    number,
    string,
    boolean,
)

from .validators import (
    required,
    length,
)

from .schema import (
    array,
    dictionary,
)


__all__ = [
    'integer',
    'number',
    'string',
    'boolean',
    'required',
    'length',
    'array',
    'dictionary',
]

__version__ = '0.3.0'
