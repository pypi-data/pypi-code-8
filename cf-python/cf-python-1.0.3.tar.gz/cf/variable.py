
from copy      import deepcopy
from re        import match as re_match
from textwrap  import fill as textwrap_fill
from itertools import izip
from cPickle   import dumps, loads, PicklingError
from re        import search as re_search
from netCDF4   import default_fillvals as _netCDF4_default_fillvals

from numpy import array       as numpy_array
from numpy import result_type as numpy_result_type

from .flags      import Flags
from .functions  import RTOL, ATOL, equals
from .functions  import inspect as cf_inspect
from .query      import Query
from .units      import Units

from .data.data import Data

_units_None = Units()

## --------------------------------------------------------------------
## These methods may be weighted
## --------------------------------------------------------------------
#_weighted_collapse_methods = set(['mean', 'standard_deviation', 'variance'])
#
## --------------------------------------------------------------------
## These methods may be biased or unbiased
## --------------------------------------------------------------------
#_biased_collapse_methods = set(['standard_deviation', 'variance'])
#
## --------------------------------------------------------------------
## Map each collapse method to its corresponding cf.Data method
## --------------------------------------------------------------------
#_collapse_methods = {'mean'              : 'average',
#                     'maximum'           : 'amax',
#                     'mid_range'         : 'mid_range',
#                     'minimum'           : 'amin',
#                     'standard_deviation': 'std',
#                     'sum'               : 'sum',
#                     'variance'          : 'var',
#                     }

# ====================================================================
#
# Variable object
#
# ====================================================================

class Variable(object):
    '''

Base class for storing a data array with metadata.

A variable contains a data array and metadata comprising properties to
describe the physical nature of the data.

All components of a variable are optional.

'''
    # Define the reserved attributes. These are methods which can't be
    # overwritten, as well as a few attributes.
    _reserved_attrs = ('_reserved_attrs',
                       '_insert_data'
                       '_set_Data_attributes',
                       'binary_mask',
                       'chunk',
                       'clip',
                       'copy',
                       'cos',
                       'delprop',
                       'dump',
                       'equals',
                       'expand_dims',
                       'flip',
                       'getprop',
                       'hasprop',
                       'identity',
                       'match',
                       'name',
                       'override_units',
                       'select',
                       'setprop',
                       'sin',
                       'subspace',
                       'transpose',
                       'where',
                       )

    _special_properties = set(('units', 'calendar',
                               '_FillValue', 'missing_value'))

    def __init__(self, properties={}, attributes=None, data=None, copy=True):
        '''

**Initialization**

:Parameters:

    properties : dict, optional
        Initialize a new instance with CF properties from the
        dictionary's key/value pairs.

    attributes : dict, optional
        Provide the new instance with attributes from the dictionary's
        key/value pairs.

    data : cf.Data, optional
        Provide the new instance with an N-dimensional data array.

    copy : bool, optional
        If False then do not deep copy arguments prior to
        initialization. By default arguments are deep copied.

'''
        self._fill_value = None

        # _hasbounds is True if and only if there are cell bounds.
        self._hasbounds = False

        # True if and only if there is a data array stored in
        # self.Data
        self._hasData = False

        # Initialize the _private dictionary with an empty Units
        # object
        self._private = {'special_attributes': {},
                         'simple_properties' : {},
                         }

        setprop = self.setprop
        if copy:
            for prop, value in properties.iteritems():
                setprop(prop, deepcopy(value))

            if attributes:
                for attr, value in attributes.iteritems():
                    setattr(self, attr, deepcopy(value))
#                self.__dict__.update(deepcopy(attributes))

        else:
            for prop, value in properties.iteritems():
                setprop(prop, value)

            if attributes:
#                self.__dict__.update(attributes)
                for attr, value in attributes.iteritems():
                    setattr(self, attr, value)
        #--- End: if

        if data is not None:
            self.insert_data(data, copy=copy)
        else:   
            # _hasData is True if and only if there is a data array
            # stored in self.Data
            self._hasData = False
    #--- End: def

    def __array__(self, *dtype):
        '''
'''
        if self._hasData:
            return self.data.__array__(*dtype)

        raise ValueError("%s has no numpy.ndarray interface'" %
                         self.__class__.__name__)
    #--- End: def


#    def __setattr__(self, attr, value):
#        '''
#x.__setattr__(attr, value) <==> x.attr=value
#
#'''
##        if attr in self._reserved_attrs:
##            raise AttributeError("Can't set %s reserved attribute %r" %
##                                 (self.__class__.__name__, attr))#
#
#        super(Variable, self).__setattr__(attr, value)
#    #--- End: def

    def __contains__(self, value):
        '''

Membership test operator ``in``

x.__contains__(y) <==> y in x


'''
        return self.equals(value)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def __data__(self):
        '''

'''
        if self._hasData:
            return self.data

        raise ValueError("%s has no cf.Data interface" %
                         self.__class__.__name__)
    #--- End: def

    def __delattr__(self, attr):
        '''

x.__delattr__(attr) <==> del x.attr

'''
        if attr in self._reserved_attrs:
            raise AttributeError("Can't delete reserved attribute %r" % attr)

        super(Variable, self).__delattr__(attr)
    #--- End: def

    def __getitem__(self, index):
        '''

x.__getitem__(index) <==> x[index]

Not to be confused with `subspace`.

'''
        if isinstance(index, slice):           
            if ((index.stop is None and index.start in (None, 0, -1)) or
                (index.stop == 1    and index.start == 0 and index.step > 0)):
                raise IndexError("%s index out of range (%s)" %
                                 (self.__class__.__name__, index))
        elif index not in (0, -1):
            raise IndexError("%s index out of range (%s)" %
                             (self.__class__.__name__, index))

        return self
    #--- End: def

    def __len__(self):
        '''

The built-in function `len`

x.__len__() <==> len(x)

:Examples:

>>> len(f)
1

'''
        return 1
    #--- End: def

    def __deepcopy__(self, memo):
        '''

Used if copy.deepcopy is called.

'''
        return self.copy()
    #--- End: def

    def _binary_operation(self, other, method):
        '''

Implement binary arithmetic and comparison operations on the
Variable's Data with the numpy broadcasting rules. It is intended to
be called by the binary arithmetic and comparison methods, such as
__sub__() and __lt__().

:Parameters:

    operation : str
        The binary arithmetic or comparison method name (such as
        "__imul__" or "__ge__").

:Returns:

    new : Variable
        A new Variable, or the same Variable if the operation was
        in-place.

:Examples:

>>> u = cf.Data([0, 1, 2, 3])
>>> v = cf.Data([1, 1, 3, 4])

>>> w = u._binary_operation(u, '__add__')
>>> print w.array
[1 2 5 7]

>>> w = u._binary_operation(v, '__lt__')
>>> print w.array
[ True  False  True  True]

>>> u._binary_operation(2, '__imul__')
>>> print u.array
[0 2 4 6]

'''
        if not self._hasData:
            raise ValueError( 
                "Can't apply operator %s to a %s with no Data" %                
                (method, self.__class__.__name__))

        inplace = method[2] == 'i'

        if isinstance(other, self.__class__):
            other = other.Data

        if not inplace:
            new      = self.copy(_omit_Data=True)
            new.Data = self.Data._binary_operation(other, method)

            #if not new.Data.Units.equivalent(original_units):
            #    # this is coarse!
            #    new.delprop('standard_name')
            #
            #    if hasattr(new, 'history'):
            #        history = [new.getprop('history')]
            #    else:
            #        history = []
            #
            #    history.append(new.getprop('standard_name'))
            #    history.append(method)
            #
            #    new.setprop('history', ' '.join(history))
            ##--- End: if

            return new

        else:
            self.Data._binary_operation(other, method)
            return self
    #--- End: def

    def _query_set(self, values, exact=True):
        '''
'''
        new = self.copy(_omit_Data=True)
        new.Data = self.Data._query_set(values, exact)
        return new
    #--- End: def

    def _query_contain(self, value):
        '''
'''
        new = self.copy(_omit_Data=True)
        new.Data = self.Data == value
        return new
    #--- End: def

    def _query_wi(self, value0, value1):
        '''
'''
        new = self.copy(_omit_Data=True)
        new.Data = self.Data._query_wi(value0, value1)
        return new
    #--- End: def

    def _query_wo(self, value0, value1):
        '''
'''
        new = self.copy(_omit_Data=True)
        new.Data = self.Data._query_wo(value0, value1)
        return new
    #--- End: def

    def _unary_operation(self, method):
        '''

Implement unary arithmetic operations on the data array.

:Parameters:

    method : str
        The unary arithmetic method name (such as "__abs__").

:Returns:

    new : Variable
        A new Variable.

:Examples:

>>> type(v)
<CF cf.Variable>
>>> print v.array
[1 2 -3 -4 -5]

>>> w = v._unary_operation('__abs__')
>>> print w.array
[1 2 3 4 5]

>>> w = v.__abs__()
>>> print w.array
[1 2 3 4 5]

>>> w = abs(v)
>>> print w.array
[1 2 3 4 5]

'''
        if not self._hasData:
            raise ValueError(
                "Can't apply operator %s to a %s with no Data" %                
                (method, self.__class__.__name__))

        new = self.copy(_omit_Data=True)

        new.Data = self.Data._unary_operation(method)
        
        return new
    #--- End: def

    def __add__(self, other):
        '''

The binary arithmetic operation ``+``

x.__add__(y) <==> x+y

'''
        return self._binary_operation(other, '__add__')
    #--- End: def

    def __iadd__(self, other):
        '''

The augmented arithmetic assignment ``+=``

x.__iadd__(y) <==> x+=y

'''
        return self._binary_operation(other, '__iadd__')
    #--- End: def

    def __radd__(self, other):
        '''

The binary arithmetic operation ``+`` with reflected operands

x.__radd__(y) <==> y+x

'''
        return self._binary_operation(other, '__radd__')
    #--- End: def

    def __sub__(self, other):
        '''

The binary arithmetic operation ``-``

x.__sub__(y) <==> x-y

'''
        return self._binary_operation(other, '__sub__')
    #--- End: def

    def __isub__(self, other):
        '''

The augmented arithmetic assignment ``-=``

x.__isub__(y) <==> x-=y

'''
        return self._binary_operation(other, '__isub__')
    #--- End: def

    def __rsub__(self, other):
        '''

The binary arithmetic operation ``-`` with reflected operands

x.__rsub__(y) <==> y-x

'''
        return self._binary_operation(other, '__rsub__')
    #--- End: def

    def __mul__(self, other):
        '''

The binary arithmetic operation ``*``

x.__mul__(y) <==> x*y

'''
        return self._binary_operation(other, '__mul__')
    #--- End: def

    def __imul__(self, other):
        '''

The augmented arithmetic assignment ``*=``

x.__imul__(y) <==> x*=y

'''
        return self._binary_operation(other, '__imul__')
    #--- End: def

    def __rmul__(self, other):
        '''

The binary arithmetic operation ``*`` with reflected operands

x.__rmul__(y) <==> y*x

'''
        return self._binary_operation(other, '__rmul__')
    #--- End: def

    def __div__(self, other):
        '''

The binary arithmetic operation ``/``

x.__div__(y) <==> x/y

'''
        return self._binary_operation(other, '__div__')
    #--- End: def

    def __idiv__(self, other):
        '''

The augmented arithmetic assignment ``/=``

x.__idiv__(y) <==> x/=y

'''
        return self._binary_operation(other, '__idiv__')
    #--- End: def

    def __rdiv__(self, other):
        '''

The binary arithmetic operation ``/`` with reflected operands

x.__rdiv__(y) <==> y/x

'''
        return self._binary_operation(other, '__rdiv__')
    #--- End: def

    def __floordiv__(self, other):
        '''

The binary arithmetic operation ``//``

x.__floordiv__(y) <==> x//y

'''
        return self._binary_operation(other, '__floordiv__')
    #--- End: def

    def __ifloordiv__(self, other):
        '''

The augmented arithmetic assignment ``//=``

x.__ifloordiv__(y) <==> x//=y

'''
        return self._binary_operation(other, '__ifloordiv__')
    #--- End: def

    def __rfloordiv__(self, other):
        '''

The binary arithmetic operation ``//`` with reflected operands

x.__rfloordiv__(y) <==> y//x

'''
        return self._binary_operation(other, '__rfloordiv__')
    #--- End: def

    def __truediv__(self, other):
        '''

The binary arithmetic operation ``/`` (true division)

x.__truediv__(y) <==> x/y

'''
        return self._binary_operation(other, '__truediv__')
    #--- End: def

    def __itruediv__(self, other):
        '''

The augmented arithmetic assignment ``/=`` (true division)

x.__itruediv__(y) <==> x/=y

'''
        return self._binary_operation(other, '__itruediv__')
   #--- End: def

    def __rtruediv__(self, other):
        '''

The binary arithmetic operation ``/`` (true division) with reflected
operands

x.__rtruediv__(y) <==> y/x

'''
        return self._binary_operation(other, '__rtruediv__')
    #--- End: def

    def __pow__(self, other, modulo=None):
        '''

The binary arithmetic operations ``**`` and ``pow``

x.__pow__(y) <==> x**y

'''  
        if modulo is not None:
            raise NotImplementedError("3-argument power not supported for %r" %
                                      self.__class__.__name__)

        return self._binary_operation(other, '__pow__')
    #--- End: def

    def __ipow__(self, other, modulo=None):
        '''

The augmented arithmetic assignment ``**=``

x.__ipow__(y) <==> x**=y

'''  
        if modulo is not None:
            raise NotImplementedError("3-argument power not supported for %r" %
                                      self.__class__.__name__)

        return self._binary_operation(other, '__ipow__')
    #--- End: def

    def __rpow__(self, other, modulo=None):
        '''

The binary arithmetic operations ``**`` and ``pow`` with reflected
operands

x.__rpow__(y) <==> y**x

'''  
        if modulo is not None:
            raise NotImplementedError("3-argument power not supported for %r" %
                                      self.__class__.__name__)

        return self._binary_operation(other, '__rpow__')
    #--- End: def

    def __mod__(self, other):
        '''

The binary arithmetic operation ``%``

x.__mod__(y) <==> x % y

.. versionadded:: 1.0

'''
        return self._binary_operation(other, '__mod__')
    #--- End: def

    def __imod__(self, other):
        '''

The binary arithmetic operation ``%=``

x.__imod__(y) <==> x %= y

.. versionadded:: 1.0

'''
        return self._binary_operation(other, '__imod__')
    #--- End: def

    def __rmod__(self, other):
        '''

The binary arithmetic operation ``%`` with reflected operands

x.__rmod__(y) <==> y % x

.. versionadded:: 1.0

'''
        return self._binary_operation(other, '__rmod__')
    #--- End: def
    def __eq__(self, other):
        '''

The rich comparison operator ``==``

x.__eq__(y) <==> x==y

'''
        return self._binary_operation(other, '__eq__')
    #--- End: def

    def __ne__(self, other):
        '''

The rich comparison operator ``!=``

x.__ne__(y) <==> x!=y

'''
        return self._binary_operation(other, '__ne__')
    #--- End: def

    def __ge__(self, other):
        '''

The rich comparison operator ``>=``

x.__ge__(y) <==> x>=y

'''
        return self._binary_operation(other, '__ge__')
    #--- End: def

    def __gt__(self, other):
        '''

The rich comparison operator ``>``

x.__gt__(y) <==> x>y

'''
        return self._binary_operation(other, '__gt__')
    #--- End: def

    def __le__(self, other):
        '''

The rich comparison operator ``<=``

x.__le__(y) <==> x<=y

'''
        return self._binary_operation(other, '__le__')
    #--- End: def

    def __lt__(self, other):
        '''

The rich comparison operator ``<``

x.__lt__(y) <==> x<y

'''
        return self._binary_operation(other, '__lt__')
    #--- End: def

    def __and__(self, other):
        '''

The binary bitwise operation ``&``

x.__and__(y) <==> x&y

'''
        return self._binary_operation(other, '__and__')
    #--- End: def

    def __iand__(self, other):
        '''

The augmented bitwise assignment ``&=``

x.__iand__(y) <==> x&=y

'''
        return self._binary_operation(other, '__iand__')
    #--- End: def

    def __rand__(self, other):
        '''

The binary bitwise operation ``&`` with reflected operands

x.__rand__(y) <==> y&x

'''
        return self._binary_operation(other, '__rand__')
    #--- End: def

    def __or__(self, other):
        '''

The binary bitwise operation ``|``

x.__or__(y) <==> x|y

'''
        return self._binary_operation(other, '__or__')
    #--- End: def

    def __ior__(self, other):
        '''

The augmented bitwise assignment ``|=``

x.__ior__(y) <==> x|=y

'''
        return self._binary_operation(other, '__ior__')
    #--- End: def

    def __ror__(self, other):
        '''

The binary bitwise operation ``|`` with reflected operands

x.__ror__(y) <==> y|x

'''
        return self._binary_operation(other, '__ror__')
    #--- End: def

    def __xor__(self, other):
        '''

The binary bitwise operation ``^``

x.__xor__(y) <==> x^y

'''
        return self._binary_operation(other, '__xor__')
    #--- End: def

    def __ixor__(self, other):
        '''

The augmented bitwise assignment ``^=``

x.__ixor__(y) <==> x^=y

'''
        return self._binary_operation(other, '__ixor__')
    #--- End: def

    def __rxor__(self, other):
        '''

The binary bitwise operation ``^`` with reflected operands

x.__rxor__(y) <==> y^x

'''
        return self._binary_operation(other, '__rxor__')
    #--- End: def

    def __lshift__(self, y):
        '''

The binary bitwise operation ``<<``

x.__lshift__(y) <==> x<<y

'''
        return self._binary_operation(y, '__lshift__')
    #--- End: def

    def __ilshift__(self, y):
        '''

The augmented bitwise assignment ``<<=``

x.__ilshift__(y) <==> x<<=y

'''
        return self._binary_operation(y, '__ilshift__')
    #--- End: def

    def __rlshift__(self, y):
        '''

The binary bitwise operation ``<<`` with reflected operands

x.__rlshift__(y) <==> y<<x

'''
        return self._binary_operation(y, '__rlshift__')
    #--- End: def

    def __rshift__(self, y):
        '''

The binary bitwise operation ``>>``

x.__lshift__(y) <==> x>>y

'''
        return self._binary_operation(y, '__rshift__')
    #--- End: def

    def __irshift__(self, y):
        '''

The augmented bitwise assignment ``>>=``

x.__irshift__(y) <==> x>>=y

'''
        return self._binary_operation(y, '__irshift__')
    #--- End: def

    def __rrshift__(self, y):
        '''

The binary bitwise operation ``>>`` with reflected operands

x.__rrshift__(y) <==> y>>x

'''
        return self._binary_operation(y, '__rrshift__')
    #--- End: def

    def __abs__(self):
        '''

The unary arithmetic operation ``abs``

x.__abs__() <==> abs(x)

'''
        return self._unary_operation('__abs__')
    #--- End: def

    def __neg__(self):
        '''

The unary arithmetic operation ``-``

x.__neg__() <==> -x

'''
        return self._unary_operation('__neg__')
    #--- End: def

    def __invert__(self):
        '''

The unary bitwise operation ``~``

x.__invert__() <==> ~x

'''
        return self._unary_operation('__invert__')
    #--- End: def

    def __pos__(self):
        '''

The unary arithmetic operation ``+``

x.__pos__() <==> +x

'''
        return self._unary_operation('__pos__')
    #--- End: def

    def __repr__(self):
        '''

The built-in function `repr`

x.__repr__() <==> repr(x)

'''
        name = self.name('')

        if self._hasData:
            dims = ', '.join([str(x) for x in self.shape])            
        else:
            dims = []
        dims = '(%s)' % dims

        # Units
        if self.Units._calendar:
            units = self.Units._calendar
        else:
            units = getattr(self, 'units', '')

        return '<CF %s: %s%s %s>' % (self.__class__.__name__,
                                    self.name(''), dims, units)
    #--- End: def

    def __str__(self):
        '''

The built-in function `str`

x.__str__() <==> str(x)

'''
        return self.__repr__()
    #--- End: def

    def _get_special_attr(self, attr):
        '''

'''
        d = self._private['special_attributes']
        if attr in d:
            return d[attr]

        raise AttributeError("%s doesn't have attribute %r" %
                             (self.__class__.__name__, attr))
    #--- End: def

    def _set_special_attr(self, attr, value):
        '''

'''
        self._private['special_attributes'][attr] = value
    #--- End: def

    def _del_special_attr(self, attr):
        '''

'''    
        d = self._private['special_attributes']
        if attr in d:
            del d[attr]
            return
            
        raise AttributeError("Can't delete non-existent %s attribute %r" %
                             (self.__class__.__name__, attr))
    #--- End: def

#    def _getter(self, attr):
#        '''
#
#Get an attribute from the _private dictionary.
#
#'''
#        if attr in self._private:
#            return self._private[attr]
#
#        raise AttributeError("Can't get %r attribute %r" %
#                             (self.__class__.__name__, attr))
#    #--- End: def
#
#    def _setter(self, attr, value):
#        '''
#
#Set an attribute in the _private dictionary.
#
#'''
#        self._private[attr] = value
#    #--- End: def
#
#    def _deleter(self, attr):
#        '''
#
#Deleting an attribute from the _private dictionary.
#
#'''
#        if attr in self._private:
#            del self._private[attr]
#        else:
#            raise AttributeError("Can't delete %r attribute %r" %
#                                 (self.__class__.__name__, attr))
#    #--- End: def

    def _dump_simple_properties(self, omit=(), level=0):
        '''

:Parameters:

    omit : sequence of strs, optional
        Omit the given CF properties from the description.

    level : int, optional

:Returns:

    out : str

:Examples:

'''
        indent1 = '    ' * level

        string = []

        # Simple properties
        simple = self._simple_properties()
        attrs  = sorted(set(simple) - set(omit))
        for attr in attrs:
            name   = '%s%s = ' % (indent1, attr)
            value  = repr(simple[attr])
            indent = ' ' * (len(name))
            if value.startswith("'") or value.startswith('"'):
                indent = '%(indent)s ' % locals()

            string.append(textwrap_fill(name+value, 79,
                                        subsequent_indent=indent))
        #--- End: for

        return '\n'.join(string)
    #--- End: def

    def _equivalent_data(self, other, atol=None, rtol=None, copy=True):
        '''
:Parameters:

    transpose : dict, optional

    atol : float, optional
        The absolute tolerance for all numerical comparisons, By
        default the value returned by the `cf.ATOL` function is used.

    rtol : float, optional
        The relative tolerance for all numerical comparisons, By
        default the value returned by the `cf.RTOL` function is used.

    copy : bool, optional
        If False then the *other* coordinate construct might get
        change in place.

:Returns:

    out : bool
        Whether or not the two variables have equivalent data arrays.

'''
        if self._hasData != other._hasData:
            # add traceback
            return False

        if not self._hasData:
            return True

        data0 = self.data
        data1 = other.data

        units = data0.Units
        if not units.equivalent(data1.Units):
            # add traceback
            return 

        if data0._shape != data1.shape:
            # add traceback
            return False              

        if not units.equals(data1.Units):
            if copy:
                data1 = data1.copy()
                copy = False
            data1.Units = units
        #--- End: if

        if not data0.equals(data1, rtol=rtol, atol=atol, ignore_fill_value=True):
            # add traceback
            return False

        return True
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def Data(self):
        '''

The `cf.Data` object containing the data array.

The use of this attribute does not guarantee that any missing data
value that has been set is passed on to the `cf.Data` object. Use the
`data` attribute to ensure that this is the case.

:Examples:

>>> f.Data
<CF Data: >

'''
        if self._hasData:
            return self._private['Data']

        raise AttributeError("%s doesn't have attribute 'Data'" %
                             self.__class__.__name__)
    #--- End: def
    @Data.setter
    def Data(self, value):
        private = self._private
        private['Data'] = value

        # Delete Units from the variable
        private['special_attributes'].pop('Units', None)
 
        self._hasData = True
   #--- End: def

    @Data.deleter
    def Data(self):
        private = self._private
        data = private.pop('Data', None)

        if data is None:
            raise AttributeError("Can't delete non-existent %s attribute 'Data'" %
                                 self.__class__.__name__)

        # Save the Units to the variable
        private['special_attributes']['Units'] = data.Units
        
        self._hasData = False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def data(self):
        '''

The `cf.Data` object containing the data array.

:Examples:

>>> f.data
<CF Data: [[267.3, ..., 234.5]] K>

'''
        if self._hasData:
            data = self.Data
            data.fill_value = self._fill_value
            return data 

        raise AttributeError("%s object doesn't have attribute 'data'" %
                             self.__class__.__name__)
    #--- End: def
    @data.setter
    def data(self, value):
        self.Data = value
    #--- End: def
    @data.deleter
    def data(self):
        del self.Data
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def hasbounds(self):
        '''

True if and only if there are cell bounds.

If present, cell bounds are stored in the `!bounds` attribute.

:Examples:

>>> if c.hasbounds:
...     b = c.bounds

'''
        return self._hasbounds
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def Units(self):
        '''The `cf.Units` object containing the units of the data array.

Stores the units and calendar CF properties in an internally
consistent manner. These are mirrored by the `units` and `calendar` CF
properties respectively.

:Examples:

>>> f.Units
<CF Units: K>

>>> f.Units
<CF Units: days since 2014-1-1 calendar=noleap>

        '''
        if self._hasData:
            return self.Data.Units

        try:
            return self._get_special_attr('Units')
        except AttributeError:
            self._set_special_attr('Units', _units_None)
            return _units_None
    #--- End: def

    @Units.setter
    def Units(self, value):
        if self._hasData:
            self.Data.Units = value
        else:
            self._set_special_attr('Units', value)
    #--- End: def
    @Units.deleter
    def Units(self):
        raise AttributeError(
"Can't delete %s attribute 'Units'. Use the override_units method." %
self.__class__.__name__)

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def year(self):
        '''

The year of each data array element.

Only applicable for reference time units.

'''
        x = 'year'
        if self._hasData:
            return type(self)(properties={'long_name': x},
                              data=self.data.year, copy=False)

        raise ValueError(
            "ERROR: Can't get years when there is no data array" % x)        
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def month(self):
        '''

The month of each data array element.

Only applicable for reference time units.

'''
        x = 'month'
        if self._hasData:
            return type(self)(properties={'long_name': x},
                              data=getattr(self.data, x), copy=False)

        raise ValueError(
            "ERROR: Can't get %ss when there is no data array" % x)        
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def day(self):
        '''

The day of each data array element.

Only applicable for reference time units.

'''
        x = 'day'
        if self._hasData:
            return type(self)(properties={'long_name': x},
                              data=getattr(self.data, x), copy=False)

        raise ValueError(
            "ERROR: Can't get %ss when there is no data array" % x)        
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def hour(self):
        '''

The hour of each data array element.

Only applicable for reference time units.

'''
        x = 'hour'
        if self._hasData:
            return type(self)(properties={'long_name': x},
                              data=getattr(self.data, x), copy=False)

        raise ValueError(
            "ERROR: Can't get %ss when there is no data array" % x)        
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def minute(self):
        '''

The minute of each data array element.

Only applicable for reference time units.

'''
        x = 'minute'
        if self._hasData:
            return type(self)(properties={'long_name': x},
                              data=getattr(self.data, x), copy=False)

        raise ValueError(
            "ERROR: Can't get %ss when there is no data array" % x)        
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def second(self):
        '''

The second of each data array element.

Only applicable for reference time units.

'''
        x = 'second'
        if self._hasData:
            return type(self)(properties={'long_name': x},
                              data=getattr(self.data, x), copy=False)

        raise ValueError(
            "ERROR: Can't get %ss when there is no data array" % x)        
    #--- End: def

    def max(self):
        '''The maximum of the data array.

Returns a scalar `cf.Data` object.

``f.max()`` is equivalent to ``f.data.max(squeeze=True)``.

.. seealso:: `cf.Data.max`, `mean`, `mid_range`, `min`, `range`,
             `sample_size`, `sd`, `sum`, `var`

:Examples:

>>> f.max()
<CF Data: 1052.822 hPa>

        '''
        if self._hasData:
            return self.data.max(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the maximum when there is no data array")       
    #--- End: def

    def mean(self):
        '''The unweighted mean the data array.

Returns a scalar `cf.Data` object.

``f.mean()`` is equivalent to ``f.data.mean(squeeze=True)``.

.. seealso:: `cf.Data.mean`, `max`, `mid_range`, `min`, `range`,
             `sample_size`, `sd`, `sum`, `var`

:Examples:

>>> f.mean()
<CF Data: 1002.367 hPa>

        '''
        if self._hasData:
            return self.data.mean(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the mean when there is no data array")       
    #--- End: def

    def mid_range(self):
        '''The unweighted average of the maximum and minimum of the data array.

Returns a scalar `cf.Data` object.

``f.mid_range()`` is equivalent to ``f.data.range(squeeze=True)``.

.. seealso:: `cf.Data.mid_range`, `max`, `mean`, `min`, `range`,
             `sample_size`, `sd`, `sum`, `var`

:Examples:

>>> f.mid_range()
<CF Data: 82.349 hPa>

        '''
        if self._hasData:
            return self.data.mid_range(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the mid-range when there is no data array")       
    #--- End: def

    def min(self):
        '''The minimum of the data array.

Returns a scalar `cf.Data` object.

``f.min()`` is equivalent to ``f.data.min(squeeze=True)``.

.. seealso:: `cf.Data.min`, `max`, `mean`, `mid_range`, `range`,
             `sample_size`, `sd`, `sum`, `var`

:Examples:

>>> f.min()
<CF Data: 888.125 hPa>

        '''
        if self._hasData:
            return self.data.min(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the minimum when there is no data array")       
    #--- End: def

    def range(self):
        '''The absolute difference between the maximum and minimum of the data
array.

Returns a scalar `cf.Data` object.

``f.range()`` is equivalent to ``f.data.range(squeeze=True)``.

.. seealso:: `cf.Data.range`, `max`, `mean`, `mid_range`, `min`,
             `sample_size`, `sd`, `sum`, `var`

:Examples:

>>> f.range()
<CF Data: 164.697 hPa>

        '''
        if self._hasData:
            return self.data.range(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the range when there is no data array")       
    #--- End:

    def sample_size(self):
        '''The number of non-missing data elements in the data array.

Returns a scalar `cf.Data` object.

``f.sample_size()`` is equivalent to ``f.data.sample_size(squeeze=True)``.

.. versionadded:: 1.0

.. seealso:: `cf.Data.sample_size`, `max`, `mean`, `mid_range`, `min`,
             `range`, `sd`, `sum`, `var`

:Examples:

>>> f.sample_size()
<CF Data: 7008.0>

        '''
        if self._hasData:
            return self.data.sample_size(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the sample size when there is no data array")
    #--- End: def

    def sd(self):
        '''The unweighted sample standard deviation of the data array.

Returns a scalar `cf.Data` object.

``f.sd()`` is equivalent to ``f.data.sd(ddof=1, squeeze=True)``.

.. seealso:: `cf.Data.sd`, `max`, `mean`, `mid_range`, `min`, `range`,
             `sample_size`, `sum`, `var`

:Examples:

>>> f.sd()
<CF Data: 34.458 hPa>

        '''
        if self._hasData:
            return self.data.sd(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the standard deviation when there is no data array")
    #--- End: def

    def sum(self):
        '''The sum of the data array.

Returns a scalar `cf.Data` object.

``f.sum()`` is equivalent to ``f.data.sum(squeeze=True)``.

.. seealso:: `cf.Data.sum`, `max`, `mean`, `mid_range`, `min`,
             `range`, `sample_size`, `sd`, `var`

:Examples:

>>> f.sum()
<CF Data: 17430607.321 hPa>

        '''
        if self._hasData:
            return self.data.sum(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the sum when there is no data array")       
    #--- End: def

    def var(self):
        '''The unweighted sample variance of the data array.

Returns a scalar `cf.Data` object.

``f.var()`` is equivalent to ``f.data.var(ddof=1, squeeze=True)``.

.. seealso:: `cf.Data.var`, `max`, `mean`, `mid_range`, `min`, `range`,
             `sample_size`, `sd`, `sum`

:Examples:

>>> f.var()
<CF Data: 1187.285 hPa2>

        '''
        if self._hasData:
            return self.data.var(squeeze=True)
          
        raise ValueError(
            "ERROR: Can't get the variance when there is no data array")
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def unique(self):
        '''

The unique elements of the array.

Returns a one dimensional `cf.Data` object.

:Examples:

>>> print f.array
[[4, 2, 1],
 [1, 2, 3]]
>>> print f.unique.array
[1, 2, 3, 4]
>>> f.subspace[1, -1] = cf.masked
>>> print f.unique.array
[1, 2, 4]

'''
        if self._hasData:
            return self.data.unique

        raise ValueError(
            "ERROR: Can't get unique values when there is no data array")
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def T(self):
        '''

Returns False.

.. seealso:: `X`, `Y`, `Z`

:Examples:

>>> print f.T
False

'''              
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def X(self):
        '''

Returns False.

.. seealso:: `T`, `Y`, `Z`

:Examples:

>>> print f.X
False

'''              
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def Y(self):
        '''
Returns False.

.. seealso:: `T`, `X`, `Z`

:Examples:

>>> print f.Y
False

'''              
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def Z(self):
        '''
Returns False.

.. seealso:: `T`, `X`, `Y`

:Examples:

>>> print f.Z
False

'''              
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def add_offset(self):
        '''

The add_offset CF property.

This property is only used when writing to a file on disk.

:Examples:

>>> f.add_offset = -4.0
>>> f.add_offset
-4.0
>>> del f.add_offset

>>> f.setprop('add_offset', 10.5)
>>> f.getprop('add_offset')
10.5
>>> f.delprop('add_offset')

'''
        return self.getprop('add_offset')
    #--- End: def
    @add_offset.setter
    def add_offset(self, value):
        self.setprop('add_offset', value)
        self.dtype = numpy_result_type(self.dtype, numpy_array(value).dtype)
    #--- End: def
    @add_offset.deleter
    def add_offset(self):
        self.delprop('add_offset')
        if not self.hasprop('scale_factor'):
            del self.dtype
    #--- End: def

    # ----------------------------------------------------------------
    # CF property: calendar
    # ----------------------------------------------------------------
    @property
    def calendar(self):
        '''

The calendar CF property.

:Examples:

>>> f.calendar = 'noleap'
>>> f.calendar
'noleap'
>>> del f.calendar

>>> f.setprop('calendar', 'proleptic_gregorian')
>>> f.getprop('calendar')
'proleptic_gregorian'
>>> f.delprop('calendar')

'''
        value = getattr(self.Units, 'calendar', None)
        if value is None:
            raise AttributeError("%s doesn't have CF property 'calendar'" %
                                 self.__class__.__name__)
        return value
    #--- End: def

    @calendar.setter
    def calendar(self, value):
        self.Units = Units(getattr(self, 'units', None), value)
    #--- End: def

    @calendar.deleter
    def calendar(self):
        if getattr(self, 'calendar', None) is None:
            raise AttributeError("Can't delete non-existent %s CF property 'calendar'" %
                                 self.__class__.__name__)
        
        self.Units = Units(getattr(self, 'units', None))
    #--- End: def

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def comment(self):
        '''

The comment CF property.

:Examples:

>>> f.comment = 'This simulation was done on an HP-35 calculator'
>>> f.comment
'This simulation was done on an HP-35 calculator'
>>> del f.comment

>>> f.setprop('comment', 'a comment')
>>> f.getprop('comment')
'a comment'
>>> f.delprop('comment')

'''
        return self.getprop('comment')
    #--- End: def
    @comment.setter
    def comment(self, value): self.setprop('comment', value)
    @comment.deleter
    def comment(self):        self.delprop('comment')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def _FillValue(self):
        '''

The _FillValue CF property.

Note that this attribute is primarily for writing data to disk and is
independent of the missing data mask. It may, however, get used when
unmasking data array elements.

The recommended way of retrieving the missing data value is with the
`fill_value` method.

.. seealso:: `fill_value`, `missing_value`

:Examples:

>>> f._FillValue = -1.0e30
>>> f._FillValue
-1e+30
>>> del f._FillValue

Mask the data array where it equals a missing data value:

>>> f.setitem(cf.masked, condition=f.fill_value()) DCH 

'''
        d = self._private['simple_properties']
        if '_FillValue' in d:
            return d['_FillValue']

        raise AttributeError("%s doesn't have CF property '_FillValue'" %
                             self.__class__.__name__)
    #--- End: def

    @_FillValue.setter
    def _FillValue(self, value):
#        self.setprop('_FillValue', value) 
        self._private['simple_properties']['_FillValue'] = value
        self._fill_value = self.getprop('missing_value', value)
    #--- End: def

    @_FillValue.deleter
    def _FillValue(self):
        self._private['simple_properties'].pop('_FillValue', None)
        self._fill_value = getattr(self, 'missing_value', None)
    #--- End: def

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def history(self):
        '''

The history CF property.

:Examples:

>>> f.history = 'created on 2012/10/01'
>>> f.history
'created on 2012/10/01'
>>> del f.history

>>> f.setprop('history', 'created on 2012/10/01')
>>> f.getprop('history')
'created on 2012/10/01'
>>> f.delprop('history')

'''
        return self.getprop('history')
    #--- End: def

    @history.setter
    def history(self, value): self.setprop('history', value)
    @history.deleter
    def history(self):        self.delprop('history')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def leap_month(self):
        '''

The leap_month CF property.

:Examples:

>>> f.leap_month = 2
>>> f.leap_month
2
>>> del f.leap_month

>>> f.setprop('leap_month', 11)
>>> f.getprop('leap_month')
11
>>> f.delprop('leap_month')

'''
        return self.getprop('leap_month')
    #--- End: def
    @leap_month.setter
    def leap_month(self, value): self.setprop('leap_month', value)
    @leap_month.deleter
    def leap_month(self):        self.delprop('leap_month')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def leap_year(self):
        '''

The leap_year CF property.

:Examples:

>>> f.leap_year = 1984
>>> f.leap_year
1984
>>> del f.leap_year

>>> f.setprop('leap_year', 1984)
>>> f.getprop('leap_year')
1984
>>> f.delprop('leap_year')

'''
        return self.getprop('leap_year')
    #--- End: def
    @leap_year.setter
    def leap_year(self, value): self.setprop('leap_year', value)
    @leap_year.deleter
    def leap_year(self):        self.delprop('leap_year')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def long_name(self):
        '''

The long_name CF property.

:Examples:

>>> f.long_name = 'zonal_wind'
>>> f.long_name
'zonal_wind'
>>> del f.long_name

>>> f.setprop('long_name', 'surface air temperature')
>>> f.getprop('long_name')
'surface air temperature'
>>> f.delprop('long_name')

'''
        return self.getprop('long_name')
    #--- End: def
    @long_name.setter
    def long_name(self, value): self.setprop('long_name', value)
    @long_name.deleter
    def long_name(self):        self.delprop('long_name')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def missing_value(self):
        '''

The missing_value CF property.

Note that this attribute is used primarily for writing data to disk
and is independent of the missing data mask. It may, however, be used
when unmasking data array elements.

The recommended way of retrieving the missing data value is with the
`fill_value` method.

.. seealso:: `_FillValue`, `fill_value`

:Examples:

>>> f.missing_value = 1.0e30
>>> f.missing_value
1e+30
>>> del f.missing_value

Mask the data array where it equals a missing data value:

>>> f.setitem(cf.masked, condition=f.fill_value()) DCH

'''        
        d = self._private['simple_properties']
        if 'missing_value' in d:
            return d['missing_value']

        raise AttributeError("%s doesn't have CF property 'missing_value'" %
                             self.__class__.__name__)
     #--- End: def
    @missing_value.setter
    def missing_value(self, value):
#        self.setprop('missing_value', value)
        self._private['simple_properties']['missing_value'] = value
        self._fill_value = value
    #--- End: def
    @missing_value.deleter
    def missing_value(self):
        self._private['simple_properties'].pop('missing_value', None)
        self._fill_value = getattr(self, '_FillValue', None)
    #--- End: def

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def month_lengths(self):
        '''

The month_lengths CF property.

Stored as a tuple but may be set as any array-like object.

:Examples:

>>> f.month_lengths = numpy.array([34, 31, 32, 30, 29, 27, 28, 28, 28, 32, 32, 34])
>>> f.month_lengths
(34, 31, 32, 30, 29, 27, 28, 28, 28, 32, 32, 34)
>>> del f.month_lengths

>>> f.setprop('month_lengths', [34, 31, 32, 30, 29, 27, 28, 28, 28, 32, 32, 34])
>>> f.getprop('month_lengths')
(34, 31, 32, 30, 29, 27, 28, 28, 28, 32, 32, 34)
>>> f.delprop('month_lengths')

'''
        return self.getprop('month_lengths')
    #--- End: def

    @month_lengths.setter
    def month_lengths(self, value): self.setprop('month_lengths', tuple(value))
    @month_lengths.deleter
    def month_lengths(self):        self.delprop('month_lengths')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def scale_factor(self):
        '''

The scale_factor CF property.

This property is only used when writing to a file on disk.

:Examples:

>>> f.scale_factor = 10.0
>>> f.scale_factor
10.0
>>> del f.scale_factor

>>> f.setprop('scale_factor', 10.0)
>>> f.getprop('scale_factor')
10.0
>>> f.delprop('scale_factor')

'''
        return self.getprop('scale_factor')
    #--- End: def
    @scale_factor.setter
    def scale_factor(self, value): self.setprop('scale_factor', value)
    @scale_factor.deleter
    def scale_factor(self):        self.delprop('scale_factor')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def standard_name(self):
        '''

The standard_name CF property.

:Examples:

>>> f.standard_name = 'time'
>>> f.standard_name
'time'
>>> del f.standard_name

>>> f.setprop('standard_name', 'time')
>>> f.getprop('standard_name')
'time'
>>> f.delprop('standard_name')

'''
        return self.getprop('standard_name')
    #--- End: def
    @standard_name.setter
    def standard_name(self, value): self.setprop('standard_name', value)
    @standard_name.deleter
    def standard_name(self):        self.delprop('standard_name')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def units(self):
        '''

The units CF property.

:Examples:

>>> f.units = 'K'
>>> f.units
'K'
>>> del f.units

>>> f.setprop('units', 'm.s-1')
>>> f.getprop('units')
'm.s-1'
>>> f.delprop('units')

'''
        value = getattr(self.Units, 'units', None)
        if value is None:
            raise AttributeError("%s doesn't have CF property 'units'" %
                                 self.__class__.__name__)
        return value
    #--- End: def

    @units.setter
    def units(self, value):
        self.Units = Units(value, getattr(self, 'calendar', None))
    #--- End: def
    @units.deleter
    def units(self):
        if getattr(self, 'units', None) is None:
            self.Units = Units(None, getattr(self, 'calendar', None))
    #--- End: def

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def valid_max(self):
        '''

The valid_max CF property.

:Examples:

>>> f.valid_max = 100.0
>>> f.valid_max
100.0
>>> del f.valid_max

>>> f.setprop('valid_max', 100.0)
>>> f.getprop('valid_max')
100.0
>>> f.delprop('valid_max')

'''
        return self.getprop('valid_max')
    #--- End: def
    @valid_max.setter
    def valid_max(self, value): self.setprop('valid_max', value)
    @valid_max.deleter
    def valid_max(self):        self.delprop('valid_max')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def valid_min(self):
        '''

The valid_min CF property.

:Examples:

>>> f.valid_min = 8.0
>>> f.valid_min
8.0
>>> del f.valid_min

>>> f.setprop('valid_min', 8.0)
>>> f.getprop('valid_min')
8.0
>>> f.delprop('valid_min')

'''
        return self.getprop('valid_min')
    #--- End: def
    @valid_min.setter
    def valid_min(self, value): self.setprop('valid_min', value)
    @valid_min.deleter
    def valid_min(self):        self.delprop('valid_min')

    # ----------------------------------------------------------------
    # CF property
    # ----------------------------------------------------------------
    @property
    def valid_range(self):
        '''

The valid_range CF property.

Stored as a tuple but may be set as any array-like object.

:Examples:

>>> f.valid_range = numpy.array([100., 400.])
>>> f.valid_range
(100.0, 400.0)
>>> del f.valid_range

>>> f.setprop('valid_range', [100.0, 400.0])
>>> f.getprop('valid_range')
(100.0, 400.0)
>>> f.delprop('valid_range')

'''
        return tuple(self.getprop('valid_range'))
    #--- End: def
    @valid_range.setter
    def valid_range(self, value): self.setprop('valid_range', tuple(value))
    @valid_range.deleter
    def valid_range(self):        self.delprop('valid_range')

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def subspace(self):
        '''

Return a new variable whose data is subspaced.

This attribute may be indexed to select a subspace from dimension
index values.

**Subspacing by indexing**

Subspacing by dimension indices uses an extended Python slicing
syntax, which is similar numpy array indexing. There are two
extensions to the numpy indexing functionality:

* Size 1 dimensions are never removed.

  An integer index i takes the i-th element but does not reduce the
  rank of the output array by one.

* When advanced indexing is used on more than one dimension, the
  advanced indices work independently.

  When more than one dimension's slice is a 1-d boolean array or 1-d
  sequence of integers, then these indices work independently along
  each dimension (similar to the way vector subscripts work in
  Fortran), rather than by their elements.

:Examples:

'''
        return SubspaceVariable(self)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def shape(self):
        '''

Tuple of the data array's dimension sizes.

:Examples:

>>> f.shape
(73, 96)

'''
        if self._hasData:
            return tuple(self.Data.shape)

        raise AttributeError("%s doesn't have attribute 'shape'" %
                             self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def ndim(self):
        '''

Number of dimensions in the data array.

:Examples:

>>> f.shape
(73, 96)
>>> f.ndim
2

'''
        if self._hasData:
            return self.Data.ndim

        raise AttributeError("%s doesn't have attribute 'ndim'" %
                             self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def size(self):
        '''

Number of elements in the data array.

:Examples:

>>> f.shape
(73, 96)
>>> f.size
7008

'''
        if self._hasData:
            return self.Data.size
        
        raise AttributeError("%s doesn't have attribute 'size'" %
                             self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def dtarray(self):
        '''

An independent numpy array of date-time objects.

Only applicable for reference time units.

If the calendar has not been set then the CF default calendar will be
used and the units will be updated accordingly.

The data type of the data array is unchanged.

.. seealso:: `array`, `asdatetime`, `asreftime`, `dtvarray`, `varray`

:Examples:

'''
        if self._hasData:
            return self.data.dtarray

        raise AttributeError("%s has no data array" % self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def dtype(self):
        '''

The `numpy` data type of the data array.

By default this is the data type with the smallest size and smallest
scalar kind to which all sub-arrays of the master data array may be
safely cast without loss of information. For example, if the
sub-arrays have data types 'int64' and 'float32' then the master data
array's data type will be 'float64'; or if the sub-arrays have data
types 'int64' and 'int32' then the master data array's data type will
be 'int64'.

Setting the data type to a `numpy.dtype` object, or any object
convertible to a `numpy.dtype` object, will cause the master data
array elements to be recast to the specified type at the time that
they are next accessed, and not before. This does not immediately
change the master data array elements, so, for example, reinstating
the original data type prior to data access results in no loss of
information.

Deleting the data type forces the default behaviour. Note that if the
data type of any sub-arrays has changed after `dtype` has been set
(which could occur if the data array is accessed) then the reinstated
default data type may be different to the data type prior to `dtype`
being set.

:Examples:

>>> f.dtype
dtype('float64')
>>> type(f.dtype)
<type 'numpy.dtype'>

>>> print f.array
[0.5 1.5 2.5]
>>> import numpy
>>> f.dtype = numpy.dtype(int)
>>> print f.array
[0 1 2]
>>> f.dtype = bool
>>> print f.array
[False  True  True]
>>> f.dtype = 'float64'
>>> print f.array
[ 0.  1.  1.]

>>> print f.array
[0.5 1.5 2.5]
>>> f.dtype = int
>>> f.dtype = bool
>>> f.dtype = float
>>> print f.array
[ 0.5  1.5  2.5]

'''
        if self._hasData:
            return self.Data.dtype

        raise AttributeError("%s doesn't have attribute 'dtype'" %
                             self.__class__.__name__)
    #--- End: def
    @dtype.setter
    def dtype(self, value):
        if self._hasData:
            self.Data.dtype = value
    #--- End: def
    @dtype.deleter
    def dtype(self):
        if self._hasData:
            del self.Data.dtype
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def dtvarray(self):
        '''

A numpy array view the data array converted to date-time objects.

Only applicable for reference time units.

If the calendar has not been set then the CF default calendar will be
used and the units will be updated accordingly.

.. seealso:: `array`, `asdatetime`, `asreftime`, `dtarray`, `varray`

:Examples:

'''
        if self._hasData:
            return self.data.dtvarray

        raise AttributeError("%s has no data array" % self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read/write only)
    # ----------------------------------------------------------------
    @property
    def hardmask(self):
        '''

Whether the mask is hard (True) or soft (False).

When the mask is hard, masked elements of the data array can not be
unmasked by assignment, but unmasked elements may be still be masked.

When the mask is soft, masked entries of the data array may be
unmasked by assignment and unmasked entries may be masked.

By default, the mask is hard.

.. seealso:: `where`, `subspace`

:Examples:

>>> f.hardmask = False
>>> f.hardmask
False

'''
        if self._hasData:
            return self.Data.hardmask

        raise AttributeError("%s doesn't have attribute 'hardmask'" %
                             self.__class__.__name__)
    #--- End: def
    @hardmask.setter
    def hardmask(self, value):
        if self._hasData:
            self.Data.hardmask = value
        else:
            raise AttributeError("%s doesn't have attribute 'hardmask'" %
                                 self.__class__.__name__)
    #--- End: def
    @hardmask.deleter
    def hardmask(self):
        raise AttributeError("Won't delete %s attribute 'hardmask'" %
                             self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def array(self):
        '''

A numpy array deep copy of the data array.

Changing the returned numpy array does not change the data array.

:Examples:

>>> a = f.array
>>> type(a)
<type 'numpy.ndarray'>
>>> print a
[0 1 2 3 4]
>>> a[0] = 999
>>> print a
[999 1 2 3 4]
>>> print f.array
[0 1 2 3 4]

'''
        if self._hasData:
            return self.data.array

        raise AttributeError("%s has no data array" % self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def unsafe_array(self):
        '''

'''
        if self._hasData:
            return self.data.unsafe_array

        raise AttributeError("%s has no data array" % self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def varray(self):
        '''

A numpy array view of the data array.

Changing the elements of the returned view changes the data array.

:Examples:

>>> a = f.varray
>>> type(a)
<type 'numpy.ndarray'>
>>> a
array([0, 1, 2, 3, 4])
>>> a[0] = 999
>>> f.varray
array([999, 1, 2, 3, 4])

'''
        if self._hasData:
            return self.data.varray

        raise AttributeError("%s has no data array" % self.__class__.__name__)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def isauxiliary(self): 
        '''

Always False.

.. seealso:: `ismeasure`, `isdimension`

:Examples: 

>>> f.isauxiliary
False

'''
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def ismeasure(self): 
        '''

Always False.

.. seealso:: `isauxiliary`, `isdimension`

:Examples: 

>>> f.ismeasure
False

'''
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def isdimension(self): 
        '''

Always False.

.. seealso:: `isauxiliary`, `isdimension`

:Examples: 

>>> f.isdimension
False

'''
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def isscalar(self):
        '''

True if and only if the data array is a scalar array.

:Examples:

>>> print f.array
2
>>> f.isscalar
True

>>> print f.array
[2]
>>> f.isscalar
False

>>> print f.array
[[2, 3]]
>>> f.isscalar
False

>>> f._hasData
False
>>> f.isscalar
False

'''
        if not self._hasData:
            return False

        return self.Data.isscalar
    #--- End: if

    def _change_axis_names(self, dim_name_map):
        '''

Change the axis names of the Data object.

:Parameters:

    dim_name_map : dict

:Returns:

    None

:Examples:

>>> f._change_axis_names({'0': 'dim1', '1': 'dim2'})

'''
        if self._hasData:
            self.Data.change_axis_names(dim_name_map)
    #--- End: def

    def _parse_match(self, match):
        '''
Called by `match`
'''        
        if not match:
            return ()

        if isinstance(match, (basestring, dict, Query)):
            match = (match,)

        matches = []
        for m in match:            
            if isinstance(m, basestring):
                if ':' in m:
                    # CF property (string-valued)
                    m = m.split(':')
                    matches.append({m[0]: ':'.join(m[1:])})
                else:
                    # Identity (string-valued) or python attribute
                    # (string-valued) or axis type
                    matches.append({None: m})

            elif isinstance(m, dict):
                # Dictionary
                matches.append(m)

            else:
                # Identity (not string-valued, e.g. cf.Query).
                matches.append({None: m})
        #--- End: for

        return matches
    #--- End: def

    def ceil(self, i=False):
        '''

Return the ceiling of the data array.

.. versionadded:: 1.0

.. seealso:: `floor`, `rint`, `trunc`

:Parameters:

    i : bool, optional
        If True then update the variable in place. By default a new
        instance is created.

:Returns:

    out : 
        The variable with new data array.

:Examples:

>>> print f.array
[-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
>>> print f.ceil().array
[-1. -1. -1. -1.  0.  1.  2.  2.  2.]

'''
        if not self._hasData:
            raise ValueError("Can't ceil %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        v.Data.ceil(i=True)

        return v
    #--- End: def
        
    def chunk(self, chunksize=None):
        '''

Partition the data array.

:Parameters:

    chunksize : int

:Returns:

    None

'''
        if self._hasData:
            self.Data.chunk(chunksize)
    #--- End: def

    def clip(self, a_min, a_max, units=None, i=False):
        '''

Clip (limit) the values in the data array in place.

Given an interval, values outside the interval are clipped to the
interval edges.

Parameters :
 
    a_min : scalar

    a_max : scalar

    units : str or Units

    i : bool. optional

:Returns: 

    None

:Examples:

'''
        if i:
            v = self
        else:
            v = self.copy()

        if self._hasData:
            v.Data.clip( a_min, a_max, units=units, i=True)
        
        return v
    #--- End: def

    def close(self):
        '''

Close all files referenced by the variable.

Note that a closed file will be automatically reopened if its contents
are subsequently required.

:Returns:

    None

:Examples:

>>> v.close()

'''
        if self._hasData:
            self.Data.close()
    #--- End: def

    @classmethod
    def concatenate(cls, variables, axis=0, _preserve=True):
        '''

Join a sequence of variables together.

'''
        variable0 = variables[0]

        if len(variables) == 1:
            return variable0.copy()

        out = variable0.copy(_omit_Data=True)
        out.Data = Data.concatenate([v.Data for v in variables], axis=axis,
                                    _preserve=_preserve)
        return out
    #--- End: def

    def copy(self, _omit_Data=False, _only_Data=False, _omit_special=None):
        '''

Return a deep copy.

``f.copy()`` is equivalent to ``copy.deepcopy(f)``.

:Returns:

    out :
        The deep copy.

:Examples:

>>> g = f.copy()

'''

        new = type(self)()
#        ts = type(self)
#        new = ts.__new__(ts)

        if _only_Data:
            if self._hasData:
                new.Data = self.Data.copy()

            return new
        #--- End: if

        self_dict = self.__dict__.copy()
        
        self_private = self_dict.pop('_private')
            
        del self_dict['_hasData']
        new.__dict__['_fill_value'] = self_dict.pop('_fill_value')
        new.__dict__['_hasbounds']  = self_dict.pop('_hasbounds')

        if self_dict:
            try:
                new.__dict__.update(loads(dumps(self_dict, -1)))
            except PicklingError:
                new.__dict__.update(deepcopy(self_dict))
                
        private = {}

        if not _omit_Data and self._hasData:
            private['Data'] = self_private['Data'].copy()
            new._hasData = True
    
        special = self_private['special_attributes'].copy()
        if _omit_special:            
            for prop in _omit_special:
                special.pop(prop, None)
        #--- End: if

        for prop, value in special.iteritems():
            special[prop] = value.copy()

        private['special_attributes'] = special

        try:
            private['simple_properties'] = loads(dumps(self_private['simple_properties'], -1))
        except PicklingError:
            private['simple_properties'] = deepcopy(self_private['simple_properties'])
           
        new._private = private

        return new
    #--- End: def

    def cos(self, i=False):
        '''

Take the trigonometric cosine of the data array.

Units are accounted for in the calculation, so that the the cosine of
90 degrees_east is 0.0, as is the sine of 1.57079632 radians. If the
units are not equivalent to radians (such as Kelvin) then they are
treated as if they were radians.

The Units are changed to '1' (nondimensionsal).

:Parameters:

    i : bool, optional

:Returns:

    out : cf.Variable

:Examples:

>>> f.Units
<CF Units: degrees_east>
>>> print f.array
[[-90 0 90 --]]
>>> f.cos()
>>> f.Units
<CF Units: 1>
>>> print f.array
[[0.0 1.0 0.0 --]]

>>> f.Units
<CF Units: m s-1>
>>> print f.array
[[1 2 3 --]]
>>> f.cos()
>>> f.Units
<CF Units: 1>
>>> print f.array
[[0.540302305868 -0.416146836547 -0.9899924966 --]]

'''
        if i:
            v = self
        else:
            v = self.copy()

        if v._hasData:
            v.Data.cos(i=True)

        return v
    #--- End: def

    def cyclic(self, axes=None, iscyclic=True):
        '''

Set the cyclicity of axes of the data array.

.. seealso:: `iscyclic`

:Parameters:

    axes : (sequence of) int
        The axes to be set. Each axis is identified by its integer
        position. By default no axes are set.
        
    iscyclic: bool, optional
        If False then the axis is set to be non-cyclic. By default the
        axis is set to be cyclic.

:Returns:

    out : list

:Examples:

>>> f.cyclic()
[]
>>> f.cyclic(1)
[]
>>> f.cyclic()
[1]

        '''
        if self._hasData:
            return self.Data.cyclic(axes, iscyclic)
        else:
            return []
    #--- End: def
            
    def datum(self, *index):
        '''

Return an element of the data array as a standard Python scalar.

The first and last elements are always returned with ``f.datum(0)``
and ``f.datum(-1)`` respectively, even if the data array is a scalar
array or has two or more dimensions.

:Parameters:

    index : *optional*
        Specify which element to return. When no positional arguments
        are provided, the method only works for data arrays with one
        element (but any number of dimensions), and the single element
        is returned. If positional arguments are given then they must
        be one of the following:

          * An integer. This argument is interpreted as a flat index
            into the array, specifying which element to copy and
            return.
         
              Example: If the data aray shape is ``(2, 3, 6)`` then:
                * ``f.datum(0)`` is equivalent to ``f.datum(0, 0, 0)``.
                * ``f.datum(-1)`` is equivalent to ``f.datum(1, 2, 5)``.
                * ``f.datum(16)`` is equivalent to ``f.datum(0, 2, 4)``.

            If *index* is ``0`` or ``-1`` then the first or last data
            array element respecitively will be returned, even if the
            data array is a scalar array or has two or more
            dimensions.
        ..
         
          * Two or more integers. These arguments are interpreted as a
            multidimensionsal index to the array. There must be the
            same number of integers as data array dimensions.
        ..
         
          * A tuple of integers. This argument is interpreted as a
            multidimensionsal index to the array. There must be the
            same number of integers as data array dimensions.
         
              Example: ``f.datum((0, 2, 4))`` is equivalent to
              ``f.datum(0, 2, 4)``; and ``f.datum(())`` is equivalent
              to ``f.datum()``.

:Returns:

    out :
        A copy of the specified element of the array as a suitable
        Python scalar.

:Examples:

>>> print f.array
2
>>> f.datum()
2
>>> 2 == f.datum(0) == f.datum(-1) == f.datum(())
True

>>> print f.array
[[2]]
>>> 2 == f.datum() == f.datum(0) == f.datum(-1)
True
>>> 2 == f.datum(0, 0) == f.datum((-1, -1)) == f.datum(-1, 0)
True

>>> print f.array
[[4 -- 6]
 [1 2 3]]
>>> f.datum(0)
4
>>> f.datum(-1)
3
>>> f.datum(1)
masked
>>> f.datum(4)
2
>>> f.datum(-2)
2
>>> f.datum(0, 0)
4
>>> f.datum(-2, -1)
6
>>> f.datum(1, 2)
3
>>> f.datum((0, 2))
6

'''
        if not self._hasData:
            raise ValueError(
                "ERROR: Can't return an element when there is no data array")
        
        return self.Data.datum(*index)
    #--- End: def

    def dump(self, display=True, prefix=None, omit=()):
        '''

Return a string containing a full description of the instance.

:Parameters:

    display : bool, optional
        If False then return the description as a string. By default
        the description is printed, i.e. ``f.dump()`` is equivalent to
        ``print f.dump(display=False)``.

    omit : sequence of strs, optional
        Omit the given CF properties from the description.

    prefix : *optional*
        Ignored.

:Returns:

    out : None or str
        A string containing the description.

:Examples:

>>> f.dump()
Data(1, 2) = [[2999-12-01 00:00:00, 3000-12-01 00:00:00]] 360_day
axis = 'T'
standard_name = 'time'

>>> f.dump(omit=('axis',))
Data(1, 2) = [[2999-12-01 00:00:00, 3000-12-01 00:00:00]] 360_day
standard_name = 'time'

'''
        string = []

        if self._hasData:
            data = self.Data
            string.append('Data%s = %s' % (data.shape, data))
        
        string.append(self._dump_simple_properties(omit=omit))

        string = '\n'.join(string)
       
        if display:
            print string
        else:
            return string
    #--- End: def

    def equals(self, other, rtol=None, atol=None,
               ignore_fill_value=False, traceback=False, ignore=()):
        '''

True if two variables are logically equal, False otherwise.

:Parameters:

    other : 
        The object to compare for equality.

    atol : float, optional
        The absolute tolerance for all numerical comparisons, By
        default the value returned by the `cf.ATOL` function is used.

    rtol : float, optional
        The relative tolerance for all numerical comparisons, By
        default the value returned by the `cf.RTOL` function is used.

    ignore_fill_value : bool, optional
        If True then data arrays with different fill values are
        considered equal. By default they are considered unequal.

    traceback : bool, optional
        If True then print a traceback highlighting where the two
        instances differ.

    ignore : sequence, optional
        Omit these CF properties from the comparison.

:Returns: 

    out : bool
        Whether or not the two instances are equal.

:Examples:

>>> f.equals(f)
True
>>> g = f + 1
>>> f.equals(g)
False
>>> g -= 1
>>> f.equals(g)
True
>>> f.setprop('name', 'name0')
>>> g.setprop('name', 'name1')
>>> f.equals(g)
False
>>> f.equals(g, ignore=['name'])
True

'''
        # Check for object identity
        if self is other:
            return True

        # Check that each instance is the same type
        if self.__class__ != other.__class__:
            if traceback:
                print("%s: Different type: %s, %s" %
                      (self.__class__.__name__,
                       self.__class__.__name__,
                       other.__class__.__name__))
            return False
        #--- End: if

        # ------------------------------------------------------------
        # Check the simple properties
        # ------------------------------------------------------------
        if ignore_fill_value:
            ignore += ('_FillValue', 'missing_value')

        self_simple  = self._private['simple_properties']
        other_simple = other._private['simple_properties']

        if (set(self_simple).difference(ignore) != 
            set(other_simple).difference(ignore)):
            if traceback:
                print("%s: Different properties: %s, %s" % 
                      (self.__class__.__name__,
                       self_simple, other_simple))
            return False
        #--- End: if

        if rtol is None:
            rtol = RTOL()
        if atol is None:
            atol = ATOL()

        for attr, x in self_simple.iteritems():
            if attr in ignore:
                continue
            y = other_simple[attr]
            if not equals(x, y, rtol=rtol, atol=atol,
                          ignore_fill_value=ignore_fill_value,
                          traceback=traceback):
                if traceback:
                    print("%s: Different %s properties: %r, %r" %
                          (self.__class__.__name__, attr, x, y))
                return False
        #--- End: for

        # ------------------------------------------------------------
        # Check the special attributes
        # ------------------------------------------------------------
        self_special  = self._private['special_attributes']
        other_special = other._private['special_attributes']
        if set(self_special) != set(other_special):
            if traceback:
                print("%s: Different attributes: %s" %
                      (self.__class__.__name__,
                       set(self_special).symmetric_difference(other_special)))
            return False
        #--- End: if

        for attr, x in self_special.iteritems():
            y = other_special[attr]
            if not equals(x, y, rtol=rtol, atol=atol,
                          ignore_fill_value=ignore_fill_value,
                          traceback=traceback): 
                if traceback:
                    print("%s: Different %s: %r, %r" %
                          (self.__class__.__name__, attr, x, y))
                return False
        #--- End: for

        # ------------------------------------------------------------
        # Check the data
        # ------------------------------------------------------------
        self_hasData = self._hasData
        if self_hasData != other._hasData:
            if traceback:
                print("%s: Different data" % self.__class__.__name__)
            return False

        if self_hasData:
            if not self.data.equals(other.data, rtol=rtol, atol=atol,
                                    ignore_fill_value=ignore_fill_value,
                                    traceback=traceback):
                if traceback:
                    print("%s: Different data" % self.__class__.__name__)
                return False
        #--- End: if

        return True
    #--- End: def

    def floor(self, i=False):
        '''

Return the floor of the data array.

.. versionadded:: 1.0

.. seealso:: `ceil`, `rint`, `trunc`

:Parameters:

    i : bool, optional
        If True then update the variable in place. By default a new
        instance is created.

:Returns:

    out : 
        The variable with new data array.

:Examples:

>>> print f.array
[-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
>>> print f.floor().array
[-2. -2. -2. -1.  0.  1.  1.  1.  1.]

'''
        if not self._hasData:
            raise ValueError("Can't floor %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        v.Data.floor(i=True)

        return v
    #--- End: def

    def match(self, match=None, ndim=None, exact=False, match_and=True,
              inverse=False, _Flags=False, _CellMethods=False):
        '''

Determine whether or not a variable satisfies conditions.

Conditions may be specified on the variable's attributes and CF
properties.

:Parameters:

:Returns:

    out : bool
        Whether or not the variable matches the given criteria.

:Examples:

'''
        conditions_have_been_set = False
        something_has_matched    = False

        if ndim is not None:
            conditions_have_been_set = True
            try:
                found_match = self.ndim == ndim
            except AttributeError:
                found_match = False

            if match_and and not found_match:
                return bool(inverse)

            something_has_matched = True
        #--- End: if
            
        matches = self._parse_match(match)

        if matches:
            conditions_have_been_set = True

        found_match = True
        for match in matches:
            found_match = True

            # ----------------------------------------------------
            # Try to match cf.Units
            # ----------------------------------------------------
            if 'units' in match or 'calendar' in match:
                match = match.copy()
                units = Units(match.pop('units', None), match.pop('calendar', None))
                
                if not exact:
                    found_match = self.Units.equivalent(units)
                else:
                    found_match = self.Units.equals(units)
    
                if not found_match:
                    continue
            #--- End: if

            # ----------------------------------------------------
            # Try to match cell methods
            # ----------------------------------------------------
            if _CellMethods and 'cell_methods' in match:
                f_cell_methods = self.getprop('cell_methods', None)
                
                if not f_cell_methods:
                    found_match = False
                    continue

                match = match.copy()
                cell_methods = match.pop('cell_methods')

                if not exact:
                    n = len(cell_methods)
                    if n > len(f_cell_methods):
                        found_match = False
                    else:
                        found_match = f_cell_methods[-n:].equivalent(cell_methods)
                else:
                    found_match = f_cell_methods.equals(cell_methods)
                                    
                if not found_match:
                    continue
            #--- End: if

            # ---------------------------------------------------
            # Try to match cf.Flags
            # ---------------------------------------------------
            if _Flags and ('flag_masks'    in match or 
                           'flag_meanings' in match or
                           'flag_values'   in match):
                f_flags = getattr(self, Flags, None)
                
                if not f_flags:
                    found_match = False
                    continue

                match = match.copy()
                found_match = f_flags.equals(
                    Flags(flag_masks=match.pop('flag_masks', None),
                          flag_meanings=match.pop('flag_meanings', None),
                          flag_values=match.pop('flag_values', None)))
            
                if not found_match:
                    continue
            #--- End: if
             
            for prop, value in match.iteritems():
                if prop is None: 
                    if value is None:
                        continue

                    if isinstance(value, basestring):
                        if value in ('T', 'X', 'Y', 'Z'):
                            # Axis type
                            x = getattr(self, value)
                            value = True
                        else:
                            value = value.split('%')
                            if len(value) == 1:
                                value = value[0].split(':')
                                if len(value) == 1:
                                    # Identity (string-valued)
                                    x = self.identity(None)
                                    value = value[0]
                                else:
                                    # CF property (string-valued)
                                    x = self.getprop(value[0], None)
                                    value = ':'.join(value[1:])
                            else:
                                # Python attribute (string-valued)
                                x = getattr(self, value[0], None)
                                value = '%'.join(value[1:])
                    else:   
                        # Identity (not string-valued, e.g. cf.Query)
                        x = self.identity(None)
                else:                    
                    # CF property
                    x = self.getprop(prop, None)
    
                if x is None:
                    found_match = False
                elif isinstance(x, basestring) and isinstance(value, basestring):
                    if exact:
                        found_match = (value == x)
                    else:
                        found_match = re_match(value, x)
                else:	
                    found_match = (value == x)
                    try:
                        found_match == True
                    except ValueError:
                        found_match = False
                #--- End: if
     
                if not found_match:
                    break
            #--- End: for

            if found_match:
                something_has_matched = True
                break
        #--- End: for

        if match_and and not found_match:
            return bool(inverse)

        if conditions_have_been_set:
            if something_has_matched:            
                return not bool(inverse)
            else:
                return bool(inverse)
        else:
            return not bool(inverse)
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def mask(self):
        '''

A variable containing the mask of the data array.

:Examples:

>>> v
<CF Variable: air_temperature(12, 73, 96) K>
>>> m = v.mask
>>> m
<CF Variable: long_name:mask(12, 73, 96) >
>>> m.data
<CF Data: [[[True, ..., False]]] >

'''
        long_name = self.identity()
        if long_name is not None:
            long_name+= '_mask'
        else:
            long_name  = 'mask'

        return Variable(properties={'long_name': long_name},
                        data=self.Data.mask,
                        copy=False)

        # ------------------------------------------------------------
        # Note: Use Variable rather than type(self) so that subclasses
        #       also return a Variable
        # ------------------------------------------------------------

    #--- End: def
    @mask.setter
    def mask(self, value):
        raise AttributeError("Can't set %s attribute 'mask'" %
                             self.__class__.__name__)
    @mask.deleter
    def mask(self):
        raise AttributeError("Can't delete %s attribute 'mask'" %
                             self.__class__.__name__)

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def attributes(self):
        '''

A dictionary of the attributes which are not CF properties.

:Examples:

>>> f.attributes
{}
>>> f.foo = 'bar'
>>> f.attributes
{'foo': 'bar'}
>>> f.attributes.pop('foo')
'bar'
>>> f.attributes
{'foo': 'bar'}

'''
        attributes = self.__dict__.copy()

        del attributes['_hasbounds']
        del attributes['_hasData']
        del attributes['_private']

        return attributes
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def properties(self):
        '''

A dictionary of the CF properties.

:Examples:

>>> f.properties
{'_FillValue': 1e+20,
 'foo': 'bar',
 'long_name': 'Surface Air Temperature',
 'standard_name': 'air_temperature',
 'units': 'K'}

'''
        return self._simple_properties().copy()
    #--- End: def

    def all(self):
        '''

Test whether all data array elements evaluate to True.

Performs a logical and over the data array and returns the
result. Masked values are considered as True during computation.

:Examples:

>>> print f.array
[[0 3 0]]
>>> f.all()
False

>>> print f.array
[[1 3 --]]
>>> f.all()
True

'''
        if self._hasData:
            return self.Data.all()

        return False
    #--- End: def

    def allclose(self, y, atol=None, rtol=None): #, shape=False):
        '''

Returns True if two broadcastable arrays have equal values to within
numerical tolerance, False otherwise.

``d.allclose(y, atol, rtol)`` is equivalent to ``(abs(d - y) <= ``atol
+ rtol*abs(y)).all()``, unless ``d`` or ``y`` are non-numeric in which
case it is equivalent to ``(d == y).all()``.

'''
        if self._hasData:
            data = getattr(y, 'data', None)
            if data is not None:
                y = data

            return self.Data.allclose(y, atol=atol, rtol=rtol)

        return False
    #--- End: def

#    def collapse(self, method, axes=None, keepdims=False, weights=None,
#                 biased=True):
#
#        if not self._hasData:
#            raise AttributeError("%s has no data array" % self.__class__.__name__)
#        
#        if method in _biased_collapse_methods:
#            kwargs = {'biased': biased}
#        else:
#            kwargs = {}
#
#        if method in _weighted_collapse_methods:
#            kwargs = {'weights': weights}
#
#        collapse_method = getattr(self.Data, _collapse_methods[method])
#        self.Data = collapse_method(axes=axes, keepdims=keepdims, **kwargs)
#    #--- End
        
    def any(self):
        '''

Test whether any data array elements evaluate to True.

Performs a logical or over the data array and returns the
result. Masked values are considered as False during computation.

:Examples:

>>> print f.array
[[0 0 0]]
>>> f.any()
False

>>> print f.array
[[-- 0 0]]
>>> d.any()
False

>>> print f.array
[[-- 3 0]]
>>> f.any()
True

'''
        if self._hasData:
            return self.Data.any()

        return False
    #--- End: def

    def asreftime(self):
        '''

Change the internal representation of data array elements from
datatime-like objects to numeric reference times.

The change is carried out in place.

If the calendar has not been set then the CF default calendar will be
used and the units will be updated accordingly.

If the internal representations are already numeric reference times
then no change occurs.

.. seealso:: `asdatetime`

:Returns:

    None


:Examples:

>>> f.asreftime()

'''
        if self._hasData:
            return self.data.asreftime()

        raise AttributeError("%s has no data array" % self.__class__.__name__)
    #--- End: def

    def asdatetime(self):
        '''

Change the internal representation of data array elements from numeric
reference times to datatime-like objects.

The change is carried out in place.

If the calendar has not been set then the CF default calendar will be
used and the units will be updated accordingly.

If the internal representations are already datatime-like objects then
no change occurs.

.. seealso:: `asreftime`

:Returns:

    None

:Examples:

>>> f.asdatetime()

'''    
        if self._hasData:
            return self.data.asdatetime()

        raise AttributeError("%s has no data array" % self.__class__.__name__)
    #--- End: def

    def fill_value(self, default=None):
        '''
       
Return the data array missing data value.

This is the value of the `missing_value` CF property, or if that is
not set, the value of the `_FillValue` CF property, else if that is
not set, ``None``. In the last case the default `numpy` missing data
value for the array's data type is assumed if a missing data value is
required.

:Parameters:

    default : *optional*
        If the missing value is unset then return this value. By
        default, *default* is `None`. If *default* is the special
        value ``'netCDF'`` then return the netCDF default value
        appropriate to the data array's data type is used. These may
        be found as follows:

        >>> import netCDF4
        >>> print netCDF4.default_fillvals    

:Returns:

    out :
        The missing data value, or the value specified by *default* if
        one has not been set.

:Examples:

>>> f.fill_value()
None
>>> f._FillValue = -1e30
>>> f.fill_value()
-1e30
>>> f.missing_value = 1073741824
>>> f.fill_value()
1073741824
>>> del f.missing_value
>>> f.fill_value()
-1e30
>>> del f._FillValue
>>> f.fill_value()
None
>>> f,dtype
dtype('float64')
>>> f.fill_value(default='netCDF')
9.969209968386869e+36
>>> f._FillValue = -999
>>> f.fill_value(default='netCDF')
-999

'''
        fillval = self._fill_value

        if fillval is None:
            if default == 'netCDF':
                d = self.dtype
                fillval = _netCDF4_default_fillvals[d.kind + str(d.itemsize)]
            else:
                fillval = default 
        #--- End: if

        return fillval
#        return self._fill_value
    #--- End: def        

    def flip(self, axes=None, i=False):
        '''

Flip dimensions of the data array in place.

.. seealso:: `expand_dims`, `squeeze`, `transpose`

:Parameters:

    axes : (sequence of) int
        Flip the dimensions whose positions are given. By default all
        dimensions are flipped.

:Returns:

    out : cf.Variable

:Examples:

>>> f.flip()
>>> f.flip(1)
>>> f.flip([0, 1])

>>> g = f[::-1, :, ::-1]
>>> f.flip([2, 0]).equals(g)
True

'''
        if not self._hasData and (axes or axes == 0):
            raise ValueError("Can't flip %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        if v._hasData:
            v.Data.flip(axes, i=True)
        
        return v
    #--- End: def

    def mask_invalid(self, i=False):
        '''

Mask the array where invalid values occur (NaNs or infs).

Note that:

* Invalid values in the results of arithmetic operations may only
  occur if the raising of `FloatingPointError` exceptions has been
  suppressed by `cf.Data.seterr`.

* If the raising of `FloatingPointError` exceptions has been allowed
  then invalid values in the results of arithmetic operations may be
  automatically converted to masked values, depending on the setting
  of `cf.Data.mask_fpe`. In this case, such automatic conversion might
  be faster than calling `mask_invalid`.

.. seealso:: `cf.Data.mask_fpe`, `cf.Data.seterr`

:Parameters:

    i : bool, optional

:Returns:

    out : cf.Variable

:Examples:

>>> print f.array
[ 0.  1.]
>>> print g.array
[ 1.  2.]

>>> old = cf.Data.seterr('ignore')
>>> h = g/f
>>> print h.array
[ inf   2.]
>>> h.mask_invalid()
[ inf   2.]
>>> print  h.array
[--  2.]

>>> h = g**12345
>>> print h.array
[ 1.  inf]
>>> h.mask_invalid()
>>> print h.array
[1.  --]

>>> old = cf.Data.seterr('raise')
>>> old = cf.Data.mask_fpe(True)
>>> print (g/f).arary
[ --  2]
>>> print (g**12345).array
[1.  -- ]

'''
        if self._hasData:
            self.Data.mask_invalid()
    #--- End: def

    def select(self, *args, **kwargs):
        '''

Return the instance if it matches the given conditions.

``v.select(*args, **kwargs)`` is equivalent to ``v if v.match(*args,
**kwargs) else cf.List()``.

See `cf.Variable.match` for details.

:Parameters:

    args, kwargs : *optional*
        See `cf.Variable.match`.

:Returns:

    out : cf.Variable or cf.List
        If the variable matches the given conditions then it is
        returned as an object identity. Otherwise an empty `cf.List`
        object is returned.

'''
        if self.match(*args, **kwargs):
            return self
        else:
            return List()
    #--- End: def

    def binary_mask(self):
        '''

Return a binary (0 and 1) missing data mask of the data array.

The binary mask's data array comprises dimensionless 32-bit integers
and has 0 where the data array has missing data and 1 otherwise.

:Returns:

    out : Variable
        The binary mask.

:Examples:

>>> print f.mask.array
[[ True  False  True False]]
>>> b = f.binary_mask()
>>> print b.array
[[0 1 0 1]]

'''
        return type(self)(properties={'long_name': 'binary_mask'},
                          data=self.Data.binary_mask(),
                          copy=False)
    #--- End: def

    def expand_dims(self, position=0, i=False):
        '''

Insert a size 1 axis into the data array.

.. seealso:: `flip`, `squeeze`, `transpose`

:Parameters:

    position : int, optional    
        Specify the position amongst the data array axes where the new
        axis is to be inserted. By default the new axis is inserted at
        position 0, the slowest varying position.

    i : bool, optional

:Returns:

    None

:Examples:

>>> v.expand_dims(2)
>>> v.expand_dims(-1)

'''       
        if not self._hasData:
            raise ValueError(
                "Can't insert axis into %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        v.Data.expand_dims(position, i=True)
        
        return v
    #--- End: def

#    def setitem(self, value, indices=Ellipsis, condition=None, masked=None,
#                ref_mask=None, hardmask=None):
#        '''
#
#Set selected elements of the data array in place.
#
#The value to which the selected elements of the data array will be set
#may be any object which is broadcastable across the selected elements.
#
#Note the following:
#
#* ``f.setitem(value)`` is equivalent to ``f.subspace[...]=value``.
#
#* ``f.setitem(value, indices)`` is equivalent to
#  ``f.subspace[indices]=value``.
#
#* If and only if the value to be assigned is the scalar `cf.masked`
#  (or `numpy.ma.masked`) then the selected elements of data array's
#  *mask* will be set to True (masked). For example,
#  ``f.setitem(cf.masked, indices)`` is equivalent to ``f.setmask(True,
#  indices)``. This is consistent with the behaviour of numpy masked
#  arrays.
#
#:Parameters:
#
#    value : array-like
#        The value to which the selected elements of the data array
#        will be set. Must be an object which is broadcastable across
#        the selected elements.
#
#    indices : optional
#        Any indices as would be accepted by ``f.subspace``. Only
#        elements of the data array described by the indices, and where
#        other criteria (if any) are met, are set to *value*. By
#        default, the entire data array is considered. How masked
#        elements of the data array are treated depends on the
#        *hardmask* parameter. The *value* must be any object
#        broadcastable across the shape implied by *indices*. Note that
#        ``f.setitem(value, indices)`` is equivalent to
#        ``f.subspace[indices]=value``.
#
#    condition : scalar or Comparison, optional
#        A condition applied to each element of the data array
#        specified by *`indices`* which determines whether or not that
#        element is set to the logically scalar *value*. The condition
#        is evaluated by checking if each element equals the condition,
#        and if it does then that element is set to *value*. How masked
#        elements of the data array are treated depends on the
#        *hardmask* parameter. Note that if *condition* is a scalar,
#        ``x``, then this is equivalent to the Comparison object
#        ``cf.eq(x)``.
#
#    masked : bool, optional
#        If False then each unmasked element of the data array
#        specified by *ndices* is set to the logically scalar
#        *value*. If True then each unmasked element of the data array
#        specified by *indices* is unmasked and set to the logically
#        scalar *value*, regardless of the *hardmask* is parameter.
#
#    ref_mask : array-like, optional
#        Each element of the data array specified by *indices* and
#        which corresponds to an element which evaluates to False from
#        *ref_mask* is set to the logically scalar
#        *value*. *ref_mask* may be any object which is broadcastable
#        across the shape implied by *indices*. How masked elements of
#        the data array are treated depends on the *hardmask*
#        parameter.
#
#    hardmask : bool, optional
#        If True then any selected elements of the data array which are
#        masked *will not* be unmasked and assigned to. If False then
#        any selected elements of the data array which are masked
#        *will* be unmasked and assigned to. By default, the value of
#        the instance's *hardmask* attribute is used.
#
#:Returns:
#
#    None
#
#:Examples:
#
#'''
#        if not self._hasData:
#            raise ValueError(
#                "ERROR: Can't set elements when there is no data array")
#
#        self.Data.setitem(value, indices=indices, condition=condition,
#                          masked=masked, ref_mask=ref_mask,
#                          hardmask=hardmask)
#    #--- End: def
#
#    def setmask(self, value, indices=Ellipsis):
#        '''
#
#Set selected elements of the data array's mask in place.
#
#The value to which the selected elements of the mask will be set may
#be any object which is broadcastable across the selected elements. The
#broadcasted value may be of any data type but will be evaluated as
#boolean.
#
#Unmasked elements are set to the fill value.
#
#The mask may be effectively removed by setting every element to False
#with ``f.setmask(False)``.
#
#Note that if and only if the value to be assigned is logically scalar
#and evaluates to True then ``f.setmask(value, indices)`` is equivalent
#to ``f.setitem(cf.masked, indices)``. This is consistent with the
#behaviour of numpy masked arrays.
#
#:Parameters:
#
#    value : array-like
#        The value to which the selected element s of the mask will be
#        set. Must be an object which is broadcastable across the
#        selected elements.
#
#    indices : optional
#        Indices of the data array. Only elements of the mask described
#        by the indices are set to *value*. By default, the entire mask
#        is considered.
#
#:Returns:
#
#    None
#
#:Examples:
#
#'''
#        if not self._hasData:
#            raise ValueError(
#                "ERROR: Can't set the mask when there is no data array")
#
#    	self.Data.setmask(value, indices=indices)
#    #--- End: def

    def sin(self, i=False):
        '''

Take the trigonometric sine of the data array.

Units are accounted for in the calculation. For example, the the sine
of 90 degrees_east is 1.0, as is the sine of 1.57079632 radians. If
the units are not equivalent to radians (such as Kelvin) then they are
treated as if they were radians.

The Units are changed to '1' (nondimensionsal).

:Parameters:

    i : bool, optional

:Returns:

    out : cf.Variable

:Examples:

>>> f.Units
<CF Units: degrees_north>
>>> print f.array
[[-90 0 90 --]]
>>> f.sin()
>>> f.Units
<CF Units: 1>
>>> print f.array
[[-1.0 0.0 1.0 --]]

>>> f.Units
<CF Units: m s-1>
>>> print f.array
[[1 2 3 --]]
>>> f.sin()
>>> f.Units
<CF Units: 1>
>>> print f.array
[[0.841470984808 0.909297426826 0.14112000806 --]]

'''
        if i:
            v = self
        else:
            v = self.copy()
    
        if v._hasData:
            v.Data.sin(i=True)

        return v
    #--- End: def

    def tan(self, i=False):
        '''

Take the trigonometric tangent of the data array element-wise.

Units are accounted for in the calculation, so that the the tangent of
180 degrees_east is 0.0, as is the sine of 3.141592653589793
radians. If the units are not equivalent to radians (such as Kelvin)
then they are treated as if they were radians.

The Units are changed to '1' (nondimensionsal).

:Parameters:

    i : bool, optional

:Returns:

    out : cf.Coordinate

:Examples:

'''     
        if i:
            v = self
        else:
            v = self.copy()

        if v._hasData:
            v.Data.tan(i=True)

        return v
    #--- End: def

    def log(self, base=10, i=False):
        '''

Take the logarithm the data array element-wise.

:Parameters:

    base : number, optional
    
    i : bool, optional

:Returns:

    out : cf.Variable

:Examples:

>>> print f.data
[[1, ..., 6]] K
>>> print f.log().data
[[0.0, ..., 0.778151250384]] lg(re 1 K)
>>> print f.data
[[1, ..., 6]] K
>>> print f.log(2).data
>>> print f.log(2).data
[[0.0, ..., 2.58496250072]] lb(re 1 K)
>>> import math
>>> print f.log(math.e).data
[[0.0, ..., 1.79175946923]] ln(re 1 K)
>>> print f.log(4).data
[[0.0, ..., 1.29248125036]] 0.721347520444482 ln(re 1 K)

>>> g = f.log(i=True)
>>> g is f
True

'''
        if i:
            v = self
        else:
            v = self.copy()

        if v._hasData:
            v.Data.log(base, i=True)

        return v
    #--- End: def

    def squeeze(self, axes=None, i=False):
        '''

Remove size 1 dimensions from the data array in place.

.. seealso:: `expand_dims`, `flip`, `transpose`

:Parameters:

    axes : (sequence of) int, optional
        The size 1 axes to remove. By default, all size 1 axes are
        removed. Size 1 axes for removal are identified by their
        integer positions in the data array.
    
    i : bool, optional

:Returns:

    out : cf.Variable

:Examples:

>>> v.squeeze()
>>> v.squeeze(1)
>>> v.squeeze([1, 2])

'''
        if not self._hasData and (axes or axes == 0):
            raise ValueError("Can't squeeze %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        if v._hasData:
            v.Data.squeeze(axes, i=True)
        
        return v
    #--- End: def
    
    def transpose(self, axes=None, i=False):
        '''

Permute the dimensions of the data array.

.. seealso:: `expand_dims`, `flip`, `squeeze`

:Parameters:

    axes : (sequence of) int
        The new axis order of the data array. By default the order is
        reversed. Each axis of the new order is identified by its
        original integer position.
        
    i : bool, optional
        
:Returns:

    out : cf.Variable

:Examples:

>>> f.shape
(2, 3, 4)
>>> f.transpose()
>>> f.shape
(4, 3, 2)
>>> f.transpose([1, 2, 0])
>>> f.shape
(3, 2, 4)
>>> f.transpose((1, 0, 2))
>>> f.shape
(2, 3, 4)

'''
        if not self._hasData and (axes or axes == 0):
            raise ValueError("Can't transpose %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        if v._hasData:
            v.Data.transpose(axes, i=True)
        
        return v
    #--- End: def

    def trunc(self, i=False):
        '''

Return the truncated values of the data array.

The truncated value a number, ``x``, is the nearest integer which is
closer to zero than ``x`` is. In short, the fractional part of the
signed number ``x`` is discarded.

.. versionadded:: 1.0

.. seealso:: `ceil`, `floor`, `rint`

:Parameters:

    i : bool, optional
        If True then update the variable in place. By default a new
        instance is created.

:Returns:

    out : 
        The variable with new data array.

:Examples:

>>> print f.array
[-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
>>> print f.trunc().array
[-1. -1. -1. -1.  0.  1.  1.  1.  1.]

'''
        if not self._hasData:
            raise ValueError("Can't trunc %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        v.Data.trunc(i=True)

        return v
    #--- End: def

    def _simple_properties(self):
        '''

'''
        return self._private['simple_properties']
    #--- End: def

    def setprop(self, prop, value):
        '''

Set a CF property.

.. seealso:: `delprop`, `getprop`, `hasprop`

:Parameters:

    prop : str
        The name of the CF property.

    value :
        The value for the property.

:Returns:

     None

:Examples:

>>> f.setprop('standard_name', 'time')
>>> f.setprop('foo', 12.5)

'''
        # Set a special attribute
        if prop in self._special_properties:
            setattr(self, prop, value)
            return

        # Still here? Then set a simple property
        self._private['simple_properties'][prop] = value
    #--- End: def

    def hasprop(self, prop):
        '''

Return True if a CF property exists, otherise False.

.. seealso:: `delprop`, `getprop`, `setprop`

:Parameters:

    prop : str
        The name of the property.

:Returns:

     out : bool
         True if the CF property exists, otherwise False.

:Examples:

>>> f.hasprop('standard_name')
True
>>> f.hasprop('foo')
False

'''
        # Has a special property? # DCH 
        if prop in self._special_properties:
            return hasattr(self, prop)

        # Still here? Then has a simple property?
        return prop in self._private['simple_properties']
    #--- End: def

    def identity(self, default=None):
        '''Return the variable's identity.

Returns the the first found of:

* The `standard_name` CF property.

* The `!id` attribute.

* The value of the *default* parameter.

.. seealso:: `name`

:Parameters:

    default : optional
        The identity if one could not otherwise be found. By default,
        *default* is `None`.

:Returns:

    out :
        The identity.

:Examples:

>>> f.standard_name = 'Kelvin'
>>> f.id = 'foo'
>>> f.identity()
'Kelvin'
>>> del f.standard_name
>>> f.identity()
'foo'
>>> del f.id
>>> f.identity()
None
>>> f.identity('bar')
'bar'
>>> print f.identity()
None

        '''
        return self.name(default, identity=True)
    #--- End: def

    def insert_data(self, data, copy=True):
        '''

Insert a new data array into the variable in place.

:Parameters:

    data : cf.Data

    copy : bool, optional

:Returns:

    None

'''
        if not copy:
            self.Data = data
        else:
            self.Data = data.copy()
    #--- End: def

    def inspect(self):
        '''

Inspect the object for debugging.

.. seealso:: `cf.inspect`

:Returns: 

    None

:Examples:

>>> f.inspect()

'''
        print cf_inspect(self)
    #--- End: def

    def getattr(self, attr, *default):
         '''

Get a named attribute.

``f.getattr(attr, *default)`` is equivalent to ``getattr(f, attr,
*default)``.

.. seealso:: `delattr`, `hasattr`, `setattr`

:Parameters:

    attr : str
        The attribute's name.

    default : *optional*
        When a default argument is given, it is returned when the
        attribute doesn't exist; without it, an exception is raised in
        that case.

:Returns:

    out : 
        The attribute's value.

:Examples:

>>> f.foo = -99
>>> fl.getattr('foo')
-99
>>> del f.foo
>>> fl.getattr('foo', 'bar')
'bar'

'''
         return getattr(self, attr, *default)
    #--- End: def

    def hasattr(self, attr):
         '''

Return whether an attribute exists.

``f.hasattr(attr)`` is equivalent to ``hasattr(f, attr)``.

.. seealso:: `delattr`, `getattr`,  `setattr`

:Parameters:

    attr : str
        The attribute's name.

:Returns:

    out : bool
        Whether the object has the attribute.

:Examples:

>>> f.foo = -99
>>> fl.hasattr('foo')
True
>>> del f.foo
>>> fl.hasattr('foo')
False

'''
         return hasattr(self, attr)
    #--- End: def

    def getprop(self, prop, *default):
        '''

Get a CF property.

When a default argument is given, it is returned when the attribute
doesn't exist; without it, an exception is raised in that case.

.. seealso:: `delprop`, `hasprop`, `setprop`

:Parameters:

    prop : str
        The name of the CF property.

    default : optional
        Return *default* if and only if the variable does not have the
        named property.

:Returns:

    out :
        The value of the named property, or the default value.

:Raises:

    AttributeError :
        If the variable does not have the named property and a default
        value has not been set.

:Examples:

>>> f.getprop('standard_name')
>>> f.getprop('standard_name', None)
>>> f.getprop('foo')
AttributeError: Field doesn't have CF property 'foo'
>>> f.getprop('foo', 'bar')
'bar'

'''
        # Get a special attribute
        if prop in self._special_properties:
            return getattr(self, prop, *default)

        # Still here? Then get a simple attribute
        d = self._private['simple_properties']
        if default:
            return d.get(prop, default[0])
        elif prop in d:
            return d[prop]

        raise AttributeError("%s doesn't have CF property %r" %
                             (self.__class__.__name__, prop))
    #--- End: def

    def delattr(self, attr):
         '''

Delete a named attribute.

``f.delattr(attr)`` is equivalent to ``delattr(f, attr)``.

.. seealso:: `getattr`, `hasattr`, `setattr`

:Parameters:
 
    attr : str
        The attribute's name.

:Returns:

    None

:Examples:

>>> f.foo
-99
>>> f.delattr('foo')
>>> getattr(f, 'foo', 'bar')
'bar'

'''
         delattr(self, attr)
    #--- End: def

    def delprop(self, prop):
        '''

Delete a CF property.

.. seealso:: `getprop`, `hasprop`, `setprop`

:Parameters:

    prop : str
        The name of the CF property.

:Returns:

     None

:Examples:

>>> f.delprop('standard_name')
>>> f.delprop('foo')
AttributeError: Field doesn't have CF property 'foo'

'''
        # Delete a special attribute
        if prop in self._special_properties:
            delattr(self, prop)
            return

        # Still here? Then delete a simple attribut
        d = self._private['simple_properties']
        if prop in d:
            del d[prop]
        else:
            raise AttributeError("Can't delete non-existent %s CF property %r" %
                                 (self.__class__.__name__, prop))
    #--- End: def

    def name(self, default=None, identity=False, ncvar=False):
        '''Return a name for the variable.

By default the name is the first found of the following:

  1. The `standard_name` CF property.
  
  2. The `!id` attribute.
  
  3. The `long_name` CF property, preceeded by the string
     ``'long_name:'``.
  
  4. The `!ncvar` attribute, preceeded by the string ``'ncvar%'``.
  
  5. The value of the *default* parameter.

Note that ``f.name(identity=True)`` is equivalent to ``f.identity()``.

.. seealso:: `identity`

:Parameters:

    default : *optional*
        If no name can be found then return the value of the *default*
        parameter. By default the default is `None`.

    identity : bool, optional
        If True then 3. and 4. are not considered as possible names.

    ncvar : bool, optional
        If True then 1., 2. and 3. are not considered as possible
        names.

:Returns:

    out : str
        A  name for the variable.

:Examples:

>>> f.standard_name = 'air_temperature'
>>> f.long_name = 'temperature of the air'
>>> f.ncvar = 'tas'
>>> f.name()
'air_temperature'
>>> del f.standard_name
>>> f.name()
'long_name:temperature of the air'
>>> del f.long_name
>>> f.name()
'ncvar:tas'
>>> del f.ncvar
>>> f.name()
None
>>> f.name('no_name')
'no_name'
>>> f.standard_name = 'air_temperature'
>>> f.name('no_name')
'air_temperature'

        '''
        if ncvar:
            if identity:
                raise ValueError(
"Can't find identity/name: ncvar and identity parameters can't both be True")

            n = getattr(self, 'ncvar', None)
            if n is not None:
                return 'ncvar%%%s' % n
            
            return default
        #--- End: if

        n = self.getprop('standard_name', None)
        if n is not None:
            return n

        n = getattr(self, 'id', None)
        if n is not None:
            return n

        if identity:
            return default

        n = self.getprop('long_name', None)
        if n is not None:
            return 'long_name:%s' % n

        n = getattr(self, 'ncvar', None)
        if n is not None:
            return 'ncvar%%%s' % n

        return default
    #--- End: def

    def override_units(self, new_units, i=False):
        '''

Override the data array units in place.

Not to be confused with setting the `!Units` attribute to units which
are equivalent to the original units.

This is different to setting the `!Units` attribute, as the new units
need not be equivalent to the original ones and the data array
elements will not be changed to reflect the new units.

:Parameters:

    new_units : str or Units
        The new units for the data array.

    i : bool, optional

:Returns:

    out : cf.Variable

:Examples:

>>> f.Units
<CF Units: hPa>
>>> f.first_datum
100000.0
>>> f.override_units('km')
>>> f.Units
<CF Units: km>
>>> f.first_datum
100000.0
>>> f.override_units(cf.Units('watts'))
>>> f.Units
<CF Units: watts>
>>> f.first_datum
100000.0

'''
        if i:
            v = self
        else:
            v = self.copy()

        if v._hasData:
            v.Data.override_units(new_units, i=True)
        else:
            v.Units = Units(new_units)

        return v
    #--- End: def

    def rint(self, i=False):
        '''

Round elements of the data array to the nearest integer.

.. versionadded:: 1.0

.. seealso:: `ceil`, `floor`, `trunc`

:Parameters:

    i : bool, optional
        If True then update the variable in place. By default a new
        instance is created.

:Returns:

    out : 
        The variable with new data array.

:Examples:

>>> print f.array
[-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
>>> print f.rint().array
[-2. -2. -1. -1.  0.  1.  1.  2.  2.]

'''
        if not self._hasData:
            raise ValueError("Can't rint %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        v.Data.rint(i=True)

        return v
    #--- End: def

    def roll(self, axis, shift, i=False):
        '''

.. seealso:: `expand_dims`, `flip`, `squeeze`, `transpose`

:Parameters:

    axss : int
        
    i : bool, optional

:Returns:

    out : cf.Variable

:Examples:

'''
        if not self._hasData:
            raise ValueError("Can't roll %r" % self.__class__.__name__)

        if i:
            v = self
        else:
            v = self.copy()

        v.Data.roll(axis, shift, i=True)
        
        return v
    #--- End: def

    def setattr(self, attr, value):
         '''

Set a named attribute.

``f.setattr(attr, value)`` is equivalent to ``setattr(f, attr,
value)``.

.. seealso:: `delattr`, `hasattr`, `getattr`

:Parameters:

    attr : str
        The attribute's name.

    value :
        The value to set the attribute.

:Returns:

    None

:Examples:

>>> f.setattr('foo', -99)
>>> f.foo
-99

'''
     
         setattr(self, attr, value)
    #--- End: def

    def setitem(self, *args, **kwargs):
        raise NotImplementedError(
"cf.%s.setitem is dead. Use cf.%s.subspace or cf.%s.where instead." % 
(self.__class__.__name__, self.__class__.__name__, self.__class__.__name__))

    def setmask(self, *args, **kwargs):
        raise NotImplementedError(
"cf.%s.setmask is dead. Use cf.%s.subspace or cf.%s.where instead." %
(self.__class__.__name__, self.__class__.__name__, self.__class__.__name__))

    def subset(self, *args, **kwargs):
        raise NotImplementedError(
"cf.%s.subset is dead. Use cf.%s.select instead." %
(self.__class__.__name__, self.__class__.__name__))

    def where(self, condition, x, y=None, i=False):
        '''

Set data array elements depending on a condition.

.. seealso:: `cf.masked`, `hardmask`, `subspace`

:Returns:

    None

'''
        if not self._hasData:
            raise ValueError(
                "ERROR: Can't set data in nonexistent data array")
        
        if isinstance(condition, Variable):
            if not condition._hasData:
                raise ValueError(
                    "ERROR: Can't set data when %r condition has no data array" %
                    condition.__class__.__name__)
            condition = condition.Data
        #--- End: if

        if isinstance(x, Variable):
            if not x._hasData:
                raise ValueError(
                    "ERROR: Can't set data from %r with no data array" % 
                    x.__class__.__name__)
            x = x.Data
        #--- End: if

        if y is not None and isinstance(y, Variable):
            if not y._hasData:
                raise ValueError(
                    "ERROR: Can't set data from %r with no data array" %
                    y.__class__.__name__)
            y = y.Data
        #--- End: if
        
        if i:
            v = self
        else:
            v = self.copy()

        v.Data.where(condition, x, y, i=True)

        return v
    #--- End: def
#--- End: class


# ====================================================================
#
# SubspaceVariable object
#
# ====================================================================

class SubspaceVariable(object):

    __slots__ = ('variable',)

    def __init__(self, variable):
        '''

Set the contained variable.

'''
        self.variable = variable
    #--- End: def

    def __getitem__(self, indices):
        '''

Implement indexing

x.__getitem__(indices) <==> x[indices]

'''
        variable = self.variable

        new = variable.copy(_omit_Data=True)

        if variable._hasData:
            new.Data = variable.Data[indices]

        return new
   #--- End: def

    def __setitem__(self, indices, value):
        '''

Implement indexed assignment

x.__setitem__(indices, value) <==> x[indices]

'''
        if isinstance(value, Variable):
            value = value.Data

        self.variable.Data[indices] = value
    #--- End: def

#--- End: class
