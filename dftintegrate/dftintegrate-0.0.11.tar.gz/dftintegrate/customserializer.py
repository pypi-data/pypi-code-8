import numpy


def tojson(obj):
        if isinstance(obj, numpy.int64):
            return {'__class__': 'numpy.int64',
                    '__value__': int(obj)}

        if isinstance(obj, numpy.complex128):
            return {'__class__': 'numpy.complex128',
                    '__value__': [obj.real, obj.imag]}

        raise TypeError(repr(obj) + 'is not JSON serializable')
