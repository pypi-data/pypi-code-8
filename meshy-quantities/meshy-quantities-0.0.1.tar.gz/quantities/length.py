"""Units of measurement for length."""
import operator


class Length:
    """The abstract concept of a length."""
    def __init__(self, value=1):
        self.value = value

    def __str__(self):
        return '{} {}'.format(self.value, self.symbol)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '<{} object of length {}>'.format(class_name, self.value)

    def to(self, new_unit):
        """Convert to another unit of Length."""
        old_unit = self.__class__

        # When old equals new there is no conversion to perform.
        if new_unit == old_unit:
            return self

        # When old comes before new in the _conversion_table, we multiply
        try:
            factor = _conversion_table[(old_unit, new_unit)]
            method = operator.mul
        # When new comes before old in the _conversion_table, we divide
        except KeyError:
            factor = _conversion_table[(new_unit, old_unit)]
            method = operator.truediv

        new_value = method(self.value, factor)
        return new_unit(new_value)


class Metre(Length):
    symbol = 'm'


class Inch(Length):
    symbol = 'in'


class Yard(Length):
    symbol = 'yd'


INCHES_PER_YARD = 36
METRES_PER_INCH = 0.0254
METRES_PER_YARD = METRES_PER_INCH * INCHES_PER_YARD

# The factors by which lengths need be multiplied in order to convert them to
# other units. We only need to define the conversion in one direction as we
# can the calculate the reverse using division.
_conversion_table = {
    # (From, To): factor
    (Inch, Metre): METRES_PER_INCH,
    (Yard, Inch): INCHES_PER_YARD,
    (Yard, Metre): METRES_PER_YARD,
}
