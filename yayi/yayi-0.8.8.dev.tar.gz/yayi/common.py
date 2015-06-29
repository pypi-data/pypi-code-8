# -*- coding: UTF-8 -*-

#from load_libraries import YAYI
from . import COM, CORE, PIX, MEAS, IO, REC, SE

type_scalar_ui8   = COM.type(COM.c_scalar, COM.s_ui8)
type_scalar_ui16  = COM.type(COM.c_scalar, COM.s_ui16)
type_c3_ui8       = COM.type(COM.c_3, COM.s_ui8)
Ytype             = COM.type

c_scalar  = COM.c_scalar
c_3       = COM.c_3
c_complex = COM.c_complex
sUI8      = COM.s_ui8
sI8       = COM.s_i8
sUI16     = COM.s_ui16
sI16      = COM.s_i16
sFl       = COM.s_float
sDl       = COM.s_double

e_Candidate ,e_Done, e_Queued, e_Queued2, e_Watershed = (0,1,2,3,4)

Ytype     = COM.type

hex2D     = SE.SEHex2D()
hex2D.__doc__ = "Hexagonal 2D structuring element"
hex2D_nc  = SE.SEHex2D()

sq2D      = SE.SESquare2D()
#sq2D_nc   = SE.SESquare2D()

cross2D   = SE.SECross2D()
#cross2D_nc= cross2D

comparison_operations = PIX.comparison_operations


def deprecated(func):
  """This is a decorator which can be used to mark functions as deprecated. It will result in a warning being emitted when the function is used."""
  def newFunc(*args, **kwargs):
      warnings.warn("Call to deprecated function %s." % func.__name__, category=DeprecationWarning)
      return func(*args, **kwargs)
  newFunc.__name__ = func.__name__
  newFunc.__doc__ = func.__doc__
  newFunc.__dict__.update(func.__dict__)
  return newFunc

