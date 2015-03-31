"""
This module exposes the functions longlong2float() and float2longlong(),
which cast the bit pattern of a float into a long long and back.
Warning: don't use in the other direction, i.e. don't cast a random
long long to a float and back to a long long.  There are corner cases
in which it does not work.
"""

from __future__ import with_statement
from rpython.annotator import model as annmodel
from rpython.rlib.rarithmetic import r_int64
from rpython.rtyper.lltypesystem import lltype, rffi
from rpython.rtyper.extregistry import ExtRegistryEntry
from rpython.translator.tool.cbuild import ExternalCompilationInfo


# -------- implement longlong2float and float2longlong --------
DOUBLE_ARRAY_PTR = lltype.Ptr(lltype.Array(rffi.DOUBLE))
LONGLONG_ARRAY_PTR = lltype.Ptr(lltype.Array(rffi.LONGLONG))
UINT_ARRAY_PTR = lltype.Ptr(lltype.Array(rffi.UINT))
FLOAT_ARRAY_PTR = lltype.Ptr(lltype.Array(rffi.FLOAT))

# these definitions are used only in tests, when not translated
def longlong2float(llval):
    with lltype.scoped_alloc(DOUBLE_ARRAY_PTR.TO, 1) as d_array:
        ll_array = rffi.cast(LONGLONG_ARRAY_PTR, d_array)
        ll_array[0] = llval
        floatval = d_array[0]
        return floatval

def float2longlong(floatval):
    with lltype.scoped_alloc(DOUBLE_ARRAY_PTR.TO, 1) as d_array:
        ll_array = rffi.cast(LONGLONG_ARRAY_PTR, d_array)
        d_array[0] = floatval
        llval = ll_array[0]
        return llval

def uint2singlefloat_emulator(ival):
    with lltype.scoped_alloc(FLOAT_ARRAY_PTR.TO, 1) as f_array:
        i_array = rffi.cast(UINT_ARRAY_PTR, f_array)
        i_array[0] = ival
        singlefloatval = f_array[0]
        return singlefloatval

def singlefloat2uint_emulator(singlefloatval):
    with lltype.scoped_alloc(FLOAT_ARRAY_PTR.TO, 1) as f_array:
        i_array = rffi.cast(UINT_ARRAY_PTR, f_array)
        f_array[0] = singlefloatval
        ival = i_array[0]
        return ival

eci = ExternalCompilationInfo(includes=['string.h', 'assert.h'],
                              post_include_bits=["""
static float pypy__uint2singlefloat(unsigned int x) {
    float ff;
    assert(sizeof(float) == 4 && sizeof(unsigned int) == 4);
    memcpy(&ff, &x, 4);
    return ff;
}
static unsigned int pypy__singlefloat2uint(float x) {
    unsigned int ii;
    assert(sizeof(float) == 4 && sizeof(unsigned int) == 4);
    memcpy(&ii, &x, 4);
    return ii;
}
"""])

uint2singlefloat = rffi.llexternal(
    "pypy__uint2singlefloat", [rffi.UINT], rffi.FLOAT,
    _callable=uint2singlefloat_emulator, compilation_info=eci,
    _nowrapper=True, elidable_function=True, sandboxsafe=True)

singlefloat2uint = rffi.llexternal(
    "pypy__singlefloat2uint", [rffi.FLOAT], rffi.UINT,
    _callable=singlefloat2uint_emulator, compilation_info=eci,
    _nowrapper=True, elidable_function=True, sandboxsafe=True)


class Float2LongLongEntry(ExtRegistryEntry):
    _about_ = float2longlong

    def compute_result_annotation(self, s_float):
        assert annmodel.SomeFloat().contains(s_float)
        return annmodel.SomeInteger(knowntype=r_int64)

    def specialize_call(self, hop):
        [v_float] = hop.inputargs(lltype.Float)
        hop.exception_cannot_occur()
        return hop.genop("convert_float_bytes_to_longlong", [v_float], resulttype=lltype.SignedLongLong)

class LongLong2FloatEntry(ExtRegistryEntry):
    _about_ = longlong2float

    def compute_result_annotation(self, s_longlong):
        assert annmodel.SomeInteger(knowntype=r_int64).contains(s_longlong)
        return annmodel.SomeFloat()

    def specialize_call(self, hop):
        [v_longlong] = hop.inputargs(lltype.SignedLongLong)
        hop.exception_cannot_occur()
        return hop.genop("convert_longlong_bytes_to_float", [v_longlong], resulttype=lltype.Float)
