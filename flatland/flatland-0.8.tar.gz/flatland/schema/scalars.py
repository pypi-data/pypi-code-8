# -*- coding: utf-8; fill-column: 78 -*-
import datetime
import decimal
import re

from flatland._compat import (
    PY2,
    long_type,
    string_types,
    text_type,
    text_transform,
    )
from flatland.exc import AdaptationError
from flatland.signals import element_set
from flatland.util import (
    Unspecified,
    as_mapping,
    autodocument_from_superclasses,
    class_cloner,
    lazy_property,
    )
from flatland.schema.paths import pathexpr
from .base import Element


__all__ = (
    'Boolean',
    'Date',
    'DateTime',
    'Enum',
    'Float',
    'Integer',
    'Long',
    'Ref',
    'Scalar',
    'String',
    'Time',
    )


class Scalar(Element):
    """The base implementation of simple values such as a string or number.

    Scalar subclasses are responsible for translating the most common data
    types in and out of Python-native form: strings, numbers, dates, times,
    Boolean values, etc.  Any data which can be represented by a single
    ``(name, value)`` pair is a likely Scalar.

    Scalar subclasses have two responsibilities: provide a method to adapt a
    value to native Python form, and provide a method to serialize the native
    form to a string.

    This class is abstract.

    """
    flattenable = True

    validates_down = 'validators'

    def set(self, obj):
        """Process *obj* and assign the native and text values.

        :returns: True if adaptation of *obj* was successful.

        Attempts to adapt the given object and assigns this element's
        :attr:`~flatland.Element.value` and :attr:`u`
        attributes in tandem.

        If adaptation succeeds, ``.value`` will contain the
        :meth:`adapted<adapt>` native Python value and ``.u`` will contain a
        text :meth:`serialized<serialize>` version of it.  A native value
        of ``None`` will be represented as ``u''`` in ``.u``.

        If adaptation fails, ``.value`` will be ``None`` and ``.u`` will
        contain ``str(obj)`` (or unicode), or ``u''`` for none.

        """
        self.raw = obj
        try:
            # adapt and normalize the value, if possible
            obj = self.value = self.adapt(obj)
        except AdaptationError:
            self.value = None  # could not be adapted
            # but, still try to textify it
            if obj is None:
                self.u = u''
            elif isinstance(obj, text_type):
                self.u = obj
            else:
                try:
                    self.u = text_transform(obj)
                except TypeError:
                    self.u = u''
                except UnicodeDecodeError:
                    self.u = text_type(obj, errors='replace')
            element_set.send(self, adapted=False)
            return False

        # stringify it, possibly storing what we received verbatim or a
        # normalized version of it.
        if obj is None:
            self.u = u''
        else:
            self.u = self.serialize(obj)
        element_set.send(self, adapted=True)
        return True

    def adapt(self, obj):
        """Given any object *obj*, try to coerce it into native format.

        :returns: the native format or raises AdaptationError on failure.

        This abstract method is called by :meth:`set`.

        """
        raise NotImplementedError()

    def serialize(self, obj):
        """Given any object *obj*, coerce it into a text representation.

        :returns: **Must** return a Unicode text object, always.

        No special effort is made to coerce values not of native or a
        compatible type.

        This semi-abstract method is called by :meth:`set`.  The base
        implementation returns ``str(obj)`` (or unicode).

        """
        return text_transform(obj)

    def _index(self, name):
        raise IndexError(name)

    def _set_flat(self, pairs, sep):
        for key, value in pairs:
            if key == self.name:
                self.set(value)
                break

    def set_default(self):
        default = self.default_value
        if default is not Unspecified:
            self.set(default)

    def __nonzero__(self):
        return True if self.u and self.value else False

    def __str__(self):
        if PY2:
            return self.u.encode('utf8', 'replace')
        return self.u

    def __unicode__(self):
        return self.u

    def __repr__(self):
        return '<%s %r; value=%r>' % (
            type(self).__name__, self.name, self.value)


class String(Scalar):
    """A regular old text string."""

    strip = True
    """If true, strip leading and trailing whitespace during conversion."""

    def adapt(self, value):
        """Return a Python representation.

        :returns: a text value or ``None``

        If :attr:`strip` is true, leading and trailing whitespace will be
        removed.

        """
        if value is None:
            return None
        if not isinstance(value, text_type):
            value = text_transform(value)

        if self.strip:
            return value.strip()
        else:
            return value

    def serialize(self, value):
        """Return a text representation.

        :returns: a Unicode value or ``u''`` if *value* is ``None``

        If :attr:`strip` is true, leading and trailing whitespace will be
        removed.

        """
        if value is None:
            return u''
        if not isinstance(value, text_type):
            value = text_transform(value)

        if self.strip:
            return value.strip()
        else:
            return value

    @property
    def is_empty(self):
        """True if the String is missing or has no value."""
        return True if (not self.value and self.u == u'') else False


class Number(Scalar):
    """Base for numeric fields.

    Subclasses provide :attr:`type_` and :attr:`format` attributes for
    :meth:`adapt` and :meth:`serialize`.

    """

    type_ = None
    """The Python type for values, such as ``int`` or ``float``."""

    signed = True
    """If true, allow negative numbers.  Default ``True``."""

    format = u'%s'
    """The ``text`` serialization format."""

    def adapt(self, value):
        """Generic numeric coercion.

        :returns: an instance of :attr:`type_` or ``None``

        Attempt to convert *value* using the class's :attr:`type_` callable.

        """
        if value is None:
            return None
        if isinstance(value, string_types):
            value = value.strip()  # decimal.Decimal doesn't like whitespace
        try:
            native = self.type_(value)
        except (ValueError, TypeError, ArithmeticError):
            raise AdaptationError()
        else:
            if not self.signed:
                if native < self.type_():  # 0, 0.0, etc.
                    raise AdaptationError()
            return native

    def serialize(self, value):
        """Generic numeric serialization.

        :returns: Unicode text formatted with :attr:`format` or the
          ``str()`` (or unicode) of *value* if *value* is not of
          :attr:`type_`

        Converts *value* to a string using Python's string formatting function
        and the :attr:`format` as the template.  The *value* is provided to
        the format as a single, positional format argument.

        """
        if type(value) is self.type_:
            return self.format % value
        return text_transform(value)


class Integer(Number):
    """Element type for Python's int."""

    type_ = int
    """``int``"""

    format = u'%i'
    """``u'%i'``"""


class Long(Number):
    """Element type for Python's long."""

    type_ = long_type
    """``long``, or ``int`` on Python 3."""

    format = u'%i'
    """``u'%i'``"""


class Float(Number):
    """Element type for Python's float."""

    type_ = float
    """``float``"""

    format = u'%f'
    """``u'%f'``"""


class Decimal(Number):
    """Element type for Python's Decimal."""

    type_ = decimal.Decimal
    """``decimal.Decimal``"""

    format = u'%f'
    """``u'%f'``"""


class Boolean(Scalar):
    """Element type for Python's ``bool``."""

    true = u'1'
    """The text serialization for ``True``: ``u'1'``."""

    true_synonyms = (u'on', u'true', u'True', u'1')
    """A sequence of acceptable string equivalents for True.

    Defaults to ``(u'on', u'true', u'True', u'1')``
    """

    false = u''
    """The text serialization for ``False``: ``u''``."""

    false_synonyms = (u'off', u'false', u'False', u'0', u'')
    """A sequence of acceptable string equivalents for False.

    Defaults to ``(u'off', u'false', u'False', u'0', u'')``
    """

    def adapt(self, value):
        """Coerce *value* to ``bool``.

        :returns: a ``bool`` or ``None``

        If *value* is text, returns ``True`` if the value is in
        :attr:`true_synonyms`, ``False`` if in :attr:`false_synonyms` and
        ``None`` otherwise.

        For non-text values, equivalent to ``bool(value)``.

        """
        if not isinstance(value, text_type):
            return bool(value)
        elif value == self.true or value in self.true_synonyms:
            return True
        elif value == self.false or value in self.false_synonyms:
            return False
        raise AdaptationError()

    def serialize(self, value):
        """Convert ``bool(value)`` to a canonical text representation.

        :returns: either :attr:`self.true` or :attr:`self.false`.

        """
        return self.true if value else self.false


class Constrained(Scalar):
    """A scalar type with a constrained set of legal values.

    Wraps another scalar type and ensures that a value
    :meth:`~flatland.schema.base.Element.set` is within bounds defined by
    :meth:`valid_value`.  If :meth:`valid_value` returns false, the element is
    not converted and will have a :attr:`~flatland.schema.base.Element.value`
    of None.

    :class:`Constrained` is a semi-abstract class that requires an
    implementation of :meth:`valid_value`, either by subclassing or overriding
    on a per-instance basis through the constructor.

    An example of a wrapper of int values that only allows the values of 1, 2
    or 3:

      >>> from flatland import Constrained, Integer
      >>> def is_valid(element, value):
      ...     return value in (1, 2, 3)
      ...
      >>> schema = Constrained.using(child_type=Integer, valid_value=is_valid)
      >>> element = schema()
      >>> element.set(u'2')
      True
      >>> element.value
      2
      >>> element.set(u'5')
      False
      >>> element.value is None
      True

    :class:`Enum` is a subclass which provides a convenient enumerated
    wrapper.

    """

    child_type = String
    """The type of constrained value, defaulting to String."""

    def __init__(self, value=Unspecified, **kw):
        Scalar.__init__(self, **kw)
        self.child_schema = self.child_type()
        if value is not Unspecified:
            self.set(value)

    @staticmethod
    def valid_value(element, value):
        """Returns True if *value* for *element* is within the constraints.

        This method is abstract.  Override in a subclass or pass a custom
        callable to the :class:`Constrained` constructor.

        """
        return False

    def adapt(self, value):
        value = self.child_schema.adapt(value)  # may raise AdaptationError
        if not self.valid_value(self, value):
            raise AdaptationError()
        return value

    def serialize(self, value):
        return self.child_schema.serialize(value)


class Enum(Constrained):
    """A scalar type with a limited set of allowed values.

    By default values are :class:`strings<String>`, but can be of any type you
    like by customizing :attr:`~Constrained.child_type`.

    """

    @class_cloner
    def valued(cls, *enum_values):
        """Return a class with ``valid_values`` = *enum_values*

        :param \*enum_values: zero or more values for :attr:`valid_values`.
        :returns: a new class

        """
        cls.valid_values = enum_values
        return cls

    valid_values = ()
    """Valid element values.

    Attempting to :meth:`set` a value not present in *valid_values* will cause
    an adaptation failure, and :attr:`value` will be ``None``.

    """

    def __init__(self, value=Unspecified, **kw):
        Constrained.__init__(self, **kw)
        if value is not Unspecified:
            self.set(value)

    def valid_value(self, element, value):
        """True if *value* is within :attr:`valid_values`."""
        return value in self.valid_values


class Temporal(Scalar):
    """Base for datetime-based date and time fields."""

    type_ = None
    regex = None
    format = None
    used = None

    strip = True

    def adapt(self, value):
        """Coerces value to a native type.

        If *value* is an instance of :attr:`type_`, returns it unchanged.  If
        a string, attempts to parse it and construct a :attr:`type` as
        described in the attribute documentation.

        """
        if value is None:
            return value
        elif isinstance(value, self.type_):
            return value
        elif isinstance(value, string_types):
            if self.strip:
                value = value.strip()
            match = self.regex.match(value)
            if not match:
                raise AdaptationError()
            try:
                args = [int(match.group(f)) for f in self.used]
                return self.type_(*args)
            except (TypeError, ValueError):
                raise AdaptationError()
        else:
            raise AdaptationError()

    def serialize(self, value):
        """Serializes value to string.

        If *value* is an instance of :attr:`type`, formats it as described in
        the attribute documentation.  Otherwise returns ``str(value)`` (or
        unicode).

        """
        if isinstance(value, self.type_):
            return self.format % as_mapping(value)
        else:
            return text_transform(value)


class DateTime(Temporal):
    """Element type for Python datetime.datetime.

    Serializes to and from YYYY-MM-DD HH:MM:SS format.

    """

    type_ = datetime.datetime
    regex = re.compile(
        u'^(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2}) '
        u'(?P<hour>\\d{2}):(?P<minute>\\d{2}):(?P<second>\\d{2})$')
    format = (u'%(year)04i-%(month)02i-%(day)02i '
              u'%(hour)02i:%(minute)02i:%(second)02i')
    used = (u'year', u'month', u'day', u'hour', u'minute', u'second')


class Date(Temporal):
    """Element type for Python datetime.date.

    Serializes to and from YYYY-MM-DD format.

    """

    type_ = datetime.date
    regex = re.compile(
        u'^(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})$')
    format = u'%(year)04i-%(month)02i-%(day)02i'
    used = (u'year', u'month', u'day')


class Time(Temporal):
    """Element type for Python datetime.time.

    Serializes to and from HH:MM:SS format.

    """

    type_ = datetime.time
    regex = re.compile(
        u'^(?P<hour>\\d{2}):(?P<minute>\\d{2}):(?P<second>\\d{2})$')
    format = u'%(hour)02i:%(minute)02i:%(second)02i'
    used = (u'hour', u'minute', u'second')


class Ref(Scalar):
    flattenable = False

    writable = 'ignore'

    target_path = None

    @class_cloner
    def to(cls, path):
        # ensure *path* parses
        pathexpr(path)
        cls.target_path = path
        return cls

    def adapt(self, value):
        return self.target.adapt(value)

    def serialize(self, value):
        return self.target.serialize(value)

    @lazy_property
    def target(self):
        return self.find_one(self.target_path)

    def _get_u(self):
        """The text representation of the reference target."""
        return self.target.u

    def _set_u(self, ustr):
        if self.writable == 'ignore':
            return
        elif self.writable:
            self.target.u = ustr
        else:
            raise TypeError(u'Ref "%s" is not writable.' % self.name)

    u = property(_get_u, _set_u)
    del _get_u, _set_u

    def _get_value(self):
        """The native value representation of the reference target."""
        return self.target.value

    def _set_value(self, value):
        if self.writable == 'ignore':
            return
        elif self.writable:
            self.target.value = value
        else:
            raise TypeError(u'Ref "%s" is not writable.' % self.name)

    value = property(_get_value, _set_value)
    del _get_value, _set_value


for cls_name in __all__:
    autodocument_from_superclasses(globals()[cls_name])
del cls_name
