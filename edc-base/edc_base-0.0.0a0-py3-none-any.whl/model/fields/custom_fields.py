import re
from django.utils.translation import ugettext as _
from django.db import models
from django.db.models import CharField, DateTimeField, DecimalField
from django.forms import RegexField

from ...choices import DATE_ESTIMATED, IDENTITY_TYPE


class TransCharField(CharField):
    """Custom field for translation form field"""

    description = _("Custom field for translation form field")

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Translates the value."""
        if not value:  # ugettext will fail if value is None
            return value
        return _(value)

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class OtherCharField(CharField):
    """field for "Other specify" options"""

    description = _("Custom field for 'Other specify' form field")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 35)
        kwargs.setdefault('verbose_name', _('...if "Other", specify'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class DobField(DateTimeField):
    """field for date of birth"""

    description = _("Custom field for date of birth")
    # TODO: there should be a dob with and without time, validator should be installed, but is this class ever used?

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', _('Date of Birth'))
        kwargs.setdefault('editable', True)
        kwargs.setdefault('help_text', _('Format is YYYY-MM-DD'))
        # self.validators.append(datetime_is_not_future)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.DateTimeField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class IsDateEstimatedField(CharField):

    """field to question if date is estimated"""

    description = _("Custom field to question if date is estimated")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('max_length', 25)
        kwargs.setdefault('choices', DATE_ESTIMATED)
        kwargs.setdefault(
            'help_text',
            _('If the exact date is not known, please indicate which part of the date is estimated.'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class NameField(CharField):

    description = _("Custom field for Name of person")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('verbose_name', _('Name'))
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('help_text', _('Type only letters, all in uppercase and no spaces'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RegexField,
            'regex': re.compile("^[A-Z]{1,250}$"),
            'max_length': self.max_length,
            'error_messages': {
                'invalid': _(u'Enter a valid name, all letters, in uppercase and no spaces.'),
            }
        }
        defaults.update(kwargs)
        return super(NameField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class InitialsField(CharField):

    description = _("Custom field for a person\'s initials")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('verbose_name', _('Initials'))
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('help_text', _('Type 2-3 letters, all in uppercase and no spaces'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RegexField,
            'regex': re.compile("^[A-Z]{2,3}$"),
            'max_length': self.max_length,
            'error_messages': {
                'invalid': _(u'Enter valid initials. Must be 2-3 letters, all in uppercase and no spaces.'),
            }
        }
        defaults.update(kwargs)
        return super(InitialsField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class WeightField(DecimalField):
    """field for weight"""

    description = _("Custom field for weight")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('max_digits', 5)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('help_text', _('Report in kg. Format is 9.99, 99.99, etc'))
        DecimalField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DecimalField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.DecimalField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class OmangField(CharField):
    # FIXME: get rid of this if it is not encrypted!!
    """See EncryptedIdentityField!
        field for omang. If getting an ID that may alos be something other than an Omang,
        use IdentityField along with IdentityTypeField
    """

    description = _("Custom field for Botswana Omang")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('max_length', 9)
        kwargs.setdefault('help_text', _('Format is 9999[12]9999'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RegexField,
            'regex': re.compile("^[0-9]{4}[12]{1}[0-9]{4}$"),
            'max_length': self.max_length,
            'error_messages': {
                'invalid': _(u'Enter a valid Omang. Must be 9 numbers. Note that digit 5 represents gender.'),
            }
        }
        defaults.update(kwargs)
        return super(OmangField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class IdentityTypeField(CharField):

    """
        have IdentityTypeField immediately follow an identity field:

        For example,

        ...

        identity = models.CharField(
            verbose_name=_("Identity number (OMANG, etc)"),
            max_length=25,
            unique=True,
            help_text=_("Use Omang, Passport number, driver's license number or Omang receipt number")
            )

        identity_type = IdentityTypeField()

        ...

        Use the value of identity_type to check the cleaned value of identity at the form level.

    """

    description = _("Custom field for Identity Type")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', _('What type of identity number is this?'))
        kwargs.setdefault('editable', True)
        kwargs.setdefault('max_length', 15)
        kwargs.setdefault('choices', IDENTITY_TYPE)
        # kwargs.setdefault('help_text', _('Format is 9999[12]9999'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class CellPhoneField(CharField):
    """
        Custom field for bw cellphone numuber
    """
    description = _("Custom field for Cellphone numuber")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', _('Mobile'))
        kwargs.setdefault('editable', True)
        kwargs.setdefault('max_length', 8)
        kwargs.setdefault('help_text', _('The format is 99999999'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RegexField,
            'regex': re.compile("^7[1-8]{1}[0-9]{6}$"),
            'error_messages': {
                'invalid': _(u'Enter a valid cellphone number. Allowed prefixes are 71-78.'),
            }
        }
        defaults.update(kwargs)
        return super(CellPhoneField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class BloodPressureField(CharField):

    """
        Custom field for blood pressure, measured as systolic/diastolic
    """

    description = _("Custom field for Blood Pressure")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('max_length', 7)
        kwargs.setdefault(
            'help_text',
            _('The format is 999/999, but either of the two numbers can be two or three digits'))
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RegexField,
            'regex': re.compile("^[0-9]{2,3}\/[0-9]{2,3}$"),
            'max_length': self.max_length,
            'error_messages': {
                'invalid': _(u'Enter a valid blood pressure measurement. It must be systolic/diastolic.'),
            }
        }
        defaults.update(kwargs)
        return super(BloodPressureField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
