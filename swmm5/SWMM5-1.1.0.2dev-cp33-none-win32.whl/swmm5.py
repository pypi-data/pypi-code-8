# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.5
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_swmm5', [dirname(__file__)])
        except ImportError:
            import _swmm5
            return _swmm5
        if fp is not None:
            try:
                _mod = imp.load_module('_swmm5', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _swmm5 = swig_import_helper()
    del swig_import_helper
else:
    import _swmm5
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



def RunSwmmDll(inpFile, rptFile, outFile):
    return _swmm5.RunSwmmDll(inpFile, rptFile, outFile)
RunSwmmDll = _swmm5.RunSwmmDll

def OpenSwmmOutFile(outFile):
    return _swmm5.OpenSwmmOutFile(outFile)
OpenSwmmOutFile = _swmm5.OpenSwmmOutFile

def GetSwmmResult(iType, iIndex, vIndex, period):
    return _swmm5.GetSwmmResult(iType, iIndex, vIndex, period)
GetSwmmResult = _swmm5.GetSwmmResult

def CloseSwmmOutFile():
    return _swmm5.CloseSwmmOutFile()
CloseSwmmOutFile = _swmm5.CloseSwmmOutFile

def GetIDName():
    return _swmm5.GetIDName()
GetIDName = _swmm5.GetIDName

def InitGetIDName():
    return _swmm5.InitGetIDName()
InitGetIDName = _swmm5.InitGetIDName

def GetInt():
    return _swmm5.GetInt()
GetInt = _swmm5.GetInt

_swmm5.ERR_NONE_swigconstant(_swmm5)
ERR_NONE = _swmm5.ERR_NONE

_swmm5.ERR_MEMORY_swigconstant(_swmm5)
ERR_MEMORY = _swmm5.ERR_MEMORY

_swmm5.ERR_KINWAVE_swigconstant(_swmm5)
ERR_KINWAVE = _swmm5.ERR_KINWAVE

_swmm5.ERR_ODE_SOLVER_swigconstant(_swmm5)
ERR_ODE_SOLVER = _swmm5.ERR_ODE_SOLVER

_swmm5.ERR_TIMESTEP_swigconstant(_swmm5)
ERR_TIMESTEP = _swmm5.ERR_TIMESTEP

_swmm5.ERR_SUBCATCH_OUTLET_swigconstant(_swmm5)
ERR_SUBCATCH_OUTLET = _swmm5.ERR_SUBCATCH_OUTLET

_swmm5.ERR_AQUIFER_PARAMS_swigconstant(_swmm5)
ERR_AQUIFER_PARAMS = _swmm5.ERR_AQUIFER_PARAMS

_swmm5.ERR_GROUND_ELEV_swigconstant(_swmm5)
ERR_GROUND_ELEV = _swmm5.ERR_GROUND_ELEV

_swmm5.ERR_LENGTH_swigconstant(_swmm5)
ERR_LENGTH = _swmm5.ERR_LENGTH

_swmm5.ERR_ELEV_DROP_swigconstant(_swmm5)
ERR_ELEV_DROP = _swmm5.ERR_ELEV_DROP

_swmm5.ERR_ROUGHNESS_swigconstant(_swmm5)
ERR_ROUGHNESS = _swmm5.ERR_ROUGHNESS

_swmm5.ERR_BARRELS_swigconstant(_swmm5)
ERR_BARRELS = _swmm5.ERR_BARRELS

_swmm5.ERR_SLOPE_swigconstant(_swmm5)
ERR_SLOPE = _swmm5.ERR_SLOPE

_swmm5.ERR_NO_XSECT_swigconstant(_swmm5)
ERR_NO_XSECT = _swmm5.ERR_NO_XSECT

_swmm5.ERR_XSECT_swigconstant(_swmm5)
ERR_XSECT = _swmm5.ERR_XSECT

_swmm5.ERR_NO_CURVE_swigconstant(_swmm5)
ERR_NO_CURVE = _swmm5.ERR_NO_CURVE

_swmm5.ERR_PUMP_LIMITS_swigconstant(_swmm5)
ERR_PUMP_LIMITS = _swmm5.ERR_PUMP_LIMITS

_swmm5.ERR_LOOP_swigconstant(_swmm5)
ERR_LOOP = _swmm5.ERR_LOOP

_swmm5.ERR_MULTI_OUTLET_swigconstant(_swmm5)
ERR_MULTI_OUTLET = _swmm5.ERR_MULTI_OUTLET

_swmm5.ERR_DUMMY_LINK_swigconstant(_swmm5)
ERR_DUMMY_LINK = _swmm5.ERR_DUMMY_LINK

_swmm5.ERR_DIVIDER_swigconstant(_swmm5)
ERR_DIVIDER = _swmm5.ERR_DIVIDER

_swmm5.ERR_DIVIDER_LINK_swigconstant(_swmm5)
ERR_DIVIDER_LINK = _swmm5.ERR_DIVIDER_LINK

_swmm5.ERR_WEIR_DIVIDER_swigconstant(_swmm5)
ERR_WEIR_DIVIDER = _swmm5.ERR_WEIR_DIVIDER

_swmm5.ERR_NODE_DEPTH_swigconstant(_swmm5)
ERR_NODE_DEPTH = _swmm5.ERR_NODE_DEPTH

_swmm5.ERR_REGULATOR_swigconstant(_swmm5)
ERR_REGULATOR = _swmm5.ERR_REGULATOR

_swmm5.ERR_OUTFALL_swigconstant(_swmm5)
ERR_OUTFALL = _swmm5.ERR_OUTFALL

_swmm5.ERR_REGULATOR_SHAPE_swigconstant(_swmm5)
ERR_REGULATOR_SHAPE = _swmm5.ERR_REGULATOR_SHAPE

_swmm5.ERR_NO_OUTLETS_swigconstant(_swmm5)
ERR_NO_OUTLETS = _swmm5.ERR_NO_OUTLETS

_swmm5.ERR_UNITHYD_TIMES_swigconstant(_swmm5)
ERR_UNITHYD_TIMES = _swmm5.ERR_UNITHYD_TIMES

_swmm5.ERR_UNITHYD_RATIOS_swigconstant(_swmm5)
ERR_UNITHYD_RATIOS = _swmm5.ERR_UNITHYD_RATIOS

_swmm5.ERR_RDII_AREA_swigconstant(_swmm5)
ERR_RDII_AREA = _swmm5.ERR_RDII_AREA

_swmm5.ERR_RAIN_FILE_CONFLICT_swigconstant(_swmm5)
ERR_RAIN_FILE_CONFLICT = _swmm5.ERR_RAIN_FILE_CONFLICT

_swmm5.ERR_RAIN_GAGE_FORMAT_swigconstant(_swmm5)
ERR_RAIN_GAGE_FORMAT = _swmm5.ERR_RAIN_GAGE_FORMAT

_swmm5.ERR_RAIN_GAGE_TSERIES_swigconstant(_swmm5)
ERR_RAIN_GAGE_TSERIES = _swmm5.ERR_RAIN_GAGE_TSERIES

_swmm5.ERR_RAIN_GAGE_INTERVAL_swigconstant(_swmm5)
ERR_RAIN_GAGE_INTERVAL = _swmm5.ERR_RAIN_GAGE_INTERVAL

_swmm5.ERR_CYCLIC_TREATMENT_swigconstant(_swmm5)
ERR_CYCLIC_TREATMENT = _swmm5.ERR_CYCLIC_TREATMENT

_swmm5.ERR_CURVE_SEQUENCE_swigconstant(_swmm5)
ERR_CURVE_SEQUENCE = _swmm5.ERR_CURVE_SEQUENCE

_swmm5.ERR_TIMESERIES_SEQUENCE_swigconstant(_swmm5)
ERR_TIMESERIES_SEQUENCE = _swmm5.ERR_TIMESERIES_SEQUENCE

_swmm5.ERR_SNOWMELT_PARAMS_swigconstant(_swmm5)
ERR_SNOWMELT_PARAMS = _swmm5.ERR_SNOWMELT_PARAMS

_swmm5.ERR_SNOWPACK_PARAMS_swigconstant(_swmm5)
ERR_SNOWPACK_PARAMS = _swmm5.ERR_SNOWPACK_PARAMS

_swmm5.ERR_LID_TYPE_swigconstant(_swmm5)
ERR_LID_TYPE = _swmm5.ERR_LID_TYPE

_swmm5.ERR_LID_LAYER_swigconstant(_swmm5)
ERR_LID_LAYER = _swmm5.ERR_LID_LAYER

_swmm5.ERR_LID_PARAMS_swigconstant(_swmm5)
ERR_LID_PARAMS = _swmm5.ERR_LID_PARAMS

_swmm5.ERR_SUBCATCH_LID_swigconstant(_swmm5)
ERR_SUBCATCH_LID = _swmm5.ERR_SUBCATCH_LID

_swmm5.ERR_LID_AREAS_swigconstant(_swmm5)
ERR_LID_AREAS = _swmm5.ERR_LID_AREAS

_swmm5.ERR_LID_CAPTURE_AREA_swigconstant(_swmm5)
ERR_LID_CAPTURE_AREA = _swmm5.ERR_LID_CAPTURE_AREA

_swmm5.ERR_START_DATE_swigconstant(_swmm5)
ERR_START_DATE = _swmm5.ERR_START_DATE

_swmm5.ERR_REPORT_DATE_swigconstant(_swmm5)
ERR_REPORT_DATE = _swmm5.ERR_REPORT_DATE

_swmm5.ERR_REPORT_STEP_swigconstant(_swmm5)
ERR_REPORT_STEP = _swmm5.ERR_REPORT_STEP

_swmm5.ERR_INPUT_swigconstant(_swmm5)
ERR_INPUT = _swmm5.ERR_INPUT

_swmm5.ERR_LINE_LENGTH_swigconstant(_swmm5)
ERR_LINE_LENGTH = _swmm5.ERR_LINE_LENGTH

_swmm5.ERR_ITEMS_swigconstant(_swmm5)
ERR_ITEMS = _swmm5.ERR_ITEMS

_swmm5.ERR_KEYWORD_swigconstant(_swmm5)
ERR_KEYWORD = _swmm5.ERR_KEYWORD

_swmm5.ERR_DUP_NAME_swigconstant(_swmm5)
ERR_DUP_NAME = _swmm5.ERR_DUP_NAME

_swmm5.ERR_NAME_swigconstant(_swmm5)
ERR_NAME = _swmm5.ERR_NAME

_swmm5.ERR_NUMBER_swigconstant(_swmm5)
ERR_NUMBER = _swmm5.ERR_NUMBER

_swmm5.ERR_DATETIME_swigconstant(_swmm5)
ERR_DATETIME = _swmm5.ERR_DATETIME

_swmm5.ERR_RULE_swigconstant(_swmm5)
ERR_RULE = _swmm5.ERR_RULE

_swmm5.ERR_TRANSECT_UNKNOWN_swigconstant(_swmm5)
ERR_TRANSECT_UNKNOWN = _swmm5.ERR_TRANSECT_UNKNOWN

_swmm5.ERR_TRANSECT_SEQUENCE_swigconstant(_swmm5)
ERR_TRANSECT_SEQUENCE = _swmm5.ERR_TRANSECT_SEQUENCE

_swmm5.ERR_TRANSECT_TOO_FEW_swigconstant(_swmm5)
ERR_TRANSECT_TOO_FEW = _swmm5.ERR_TRANSECT_TOO_FEW

_swmm5.ERR_TRANSECT_TOO_MANY_swigconstant(_swmm5)
ERR_TRANSECT_TOO_MANY = _swmm5.ERR_TRANSECT_TOO_MANY

_swmm5.ERR_TRANSECT_MANNING_swigconstant(_swmm5)
ERR_TRANSECT_MANNING = _swmm5.ERR_TRANSECT_MANNING

_swmm5.ERR_TRANSECT_OVERBANK_swigconstant(_swmm5)
ERR_TRANSECT_OVERBANK = _swmm5.ERR_TRANSECT_OVERBANK

_swmm5.ERR_TRANSECT_NO_DEPTH_swigconstant(_swmm5)
ERR_TRANSECT_NO_DEPTH = _swmm5.ERR_TRANSECT_NO_DEPTH

_swmm5.ERR_TREATMENT_EXPR_swigconstant(_swmm5)
ERR_TREATMENT_EXPR = _swmm5.ERR_TREATMENT_EXPR

_swmm5.ERR_FILE_NAME_swigconstant(_swmm5)
ERR_FILE_NAME = _swmm5.ERR_FILE_NAME

_swmm5.ERR_INP_FILE_swigconstant(_swmm5)
ERR_INP_FILE = _swmm5.ERR_INP_FILE

_swmm5.ERR_RPT_FILE_swigconstant(_swmm5)
ERR_RPT_FILE = _swmm5.ERR_RPT_FILE

_swmm5.ERR_OUT_FILE_swigconstant(_swmm5)
ERR_OUT_FILE = _swmm5.ERR_OUT_FILE

_swmm5.ERR_OUT_WRITE_swigconstant(_swmm5)
ERR_OUT_WRITE = _swmm5.ERR_OUT_WRITE

_swmm5.ERR_OUT_READ_swigconstant(_swmm5)
ERR_OUT_READ = _swmm5.ERR_OUT_READ

_swmm5.ERR_RAIN_FILE_SCRATCH_swigconstant(_swmm5)
ERR_RAIN_FILE_SCRATCH = _swmm5.ERR_RAIN_FILE_SCRATCH

_swmm5.ERR_RAIN_FILE_OPEN_swigconstant(_swmm5)
ERR_RAIN_FILE_OPEN = _swmm5.ERR_RAIN_FILE_OPEN

_swmm5.ERR_RAIN_FILE_DATA_swigconstant(_swmm5)
ERR_RAIN_FILE_DATA = _swmm5.ERR_RAIN_FILE_DATA

_swmm5.ERR_RAIN_FILE_SEQUENCE_swigconstant(_swmm5)
ERR_RAIN_FILE_SEQUENCE = _swmm5.ERR_RAIN_FILE_SEQUENCE

_swmm5.ERR_RAIN_FILE_FORMAT_swigconstant(_swmm5)
ERR_RAIN_FILE_FORMAT = _swmm5.ERR_RAIN_FILE_FORMAT

_swmm5.ERR_RAIN_IFACE_FORMAT_swigconstant(_swmm5)
ERR_RAIN_IFACE_FORMAT = _swmm5.ERR_RAIN_IFACE_FORMAT

_swmm5.ERR_RAIN_FILE_GAGE_swigconstant(_swmm5)
ERR_RAIN_FILE_GAGE = _swmm5.ERR_RAIN_FILE_GAGE

_swmm5.ERR_RUNOFF_FILE_OPEN_swigconstant(_swmm5)
ERR_RUNOFF_FILE_OPEN = _swmm5.ERR_RUNOFF_FILE_OPEN

_swmm5.ERR_RUNOFF_FILE_FORMAT_swigconstant(_swmm5)
ERR_RUNOFF_FILE_FORMAT = _swmm5.ERR_RUNOFF_FILE_FORMAT

_swmm5.ERR_RUNOFF_FILE_END_swigconstant(_swmm5)
ERR_RUNOFF_FILE_END = _swmm5.ERR_RUNOFF_FILE_END

_swmm5.ERR_RUNOFF_FILE_READ_swigconstant(_swmm5)
ERR_RUNOFF_FILE_READ = _swmm5.ERR_RUNOFF_FILE_READ

_swmm5.ERR_HOTSTART_FILE_NAMES_swigconstant(_swmm5)
ERR_HOTSTART_FILE_NAMES = _swmm5.ERR_HOTSTART_FILE_NAMES

_swmm5.ERR_HOTSTART_FILE_OPEN_swigconstant(_swmm5)
ERR_HOTSTART_FILE_OPEN = _swmm5.ERR_HOTSTART_FILE_OPEN

_swmm5.ERR_HOTSTART_FILE_FORMAT_swigconstant(_swmm5)
ERR_HOTSTART_FILE_FORMAT = _swmm5.ERR_HOTSTART_FILE_FORMAT

_swmm5.ERR_HOTSTART_FILE_READ_swigconstant(_swmm5)
ERR_HOTSTART_FILE_READ = _swmm5.ERR_HOTSTART_FILE_READ

_swmm5.ERR_NO_CLIMATE_FILE_swigconstant(_swmm5)
ERR_NO_CLIMATE_FILE = _swmm5.ERR_NO_CLIMATE_FILE

_swmm5.ERR_CLIMATE_FILE_OPEN_swigconstant(_swmm5)
ERR_CLIMATE_FILE_OPEN = _swmm5.ERR_CLIMATE_FILE_OPEN

_swmm5.ERR_CLIMATE_FILE_READ_swigconstant(_swmm5)
ERR_CLIMATE_FILE_READ = _swmm5.ERR_CLIMATE_FILE_READ

_swmm5.ERR_CLIMATE_END_OF_FILE_swigconstant(_swmm5)
ERR_CLIMATE_END_OF_FILE = _swmm5.ERR_CLIMATE_END_OF_FILE

_swmm5.ERR_RDII_FILE_SCRATCH_swigconstant(_swmm5)
ERR_RDII_FILE_SCRATCH = _swmm5.ERR_RDII_FILE_SCRATCH

_swmm5.ERR_RDII_FILE_OPEN_swigconstant(_swmm5)
ERR_RDII_FILE_OPEN = _swmm5.ERR_RDII_FILE_OPEN

_swmm5.ERR_RDII_FILE_FORMAT_swigconstant(_swmm5)
ERR_RDII_FILE_FORMAT = _swmm5.ERR_RDII_FILE_FORMAT

_swmm5.ERR_ROUTING_FILE_OPEN_swigconstant(_swmm5)
ERR_ROUTING_FILE_OPEN = _swmm5.ERR_ROUTING_FILE_OPEN

_swmm5.ERR_ROUTING_FILE_FORMAT_swigconstant(_swmm5)
ERR_ROUTING_FILE_FORMAT = _swmm5.ERR_ROUTING_FILE_FORMAT

_swmm5.ERR_ROUTING_FILE_NOMATCH_swigconstant(_swmm5)
ERR_ROUTING_FILE_NOMATCH = _swmm5.ERR_ROUTING_FILE_NOMATCH

_swmm5.ERR_ROUTING_FILE_NAMES_swigconstant(_swmm5)
ERR_ROUTING_FILE_NAMES = _swmm5.ERR_ROUTING_FILE_NAMES

_swmm5.ERR_TABLE_FILE_OPEN_swigconstant(_swmm5)
ERR_TABLE_FILE_OPEN = _swmm5.ERR_TABLE_FILE_OPEN

_swmm5.ERR_TABLE_FILE_READ_swigconstant(_swmm5)
ERR_TABLE_FILE_READ = _swmm5.ERR_TABLE_FILE_READ

_swmm5.ERR_SYSTEM_swigconstant(_swmm5)
ERR_SYSTEM = _swmm5.ERR_SYSTEM

_swmm5.ERR_NOT_CLOSED_swigconstant(_swmm5)
ERR_NOT_CLOSED = _swmm5.ERR_NOT_CLOSED

_swmm5.ERR_NOT_OPEN_swigconstant(_swmm5)
ERR_NOT_OPEN = _swmm5.ERR_NOT_OPEN

_swmm5.ERR_FILE_SIZE_swigconstant(_swmm5)
ERR_FILE_SIZE = _swmm5.ERR_FILE_SIZE

_swmm5.MAXERRMSG_swigconstant(_swmm5)
MAXERRMSG = _swmm5.MAXERRMSG

def error_getMsg(i):
    return _swmm5.error_getMsg(i)
error_getMsg = _swmm5.error_getMsg

def error_getCode(i):
    return _swmm5.error_getCode(i)
error_getCode = _swmm5.error_getCode

def error_setInpError(errcode, s):
    return _swmm5.error_setInpError(errcode, s)
error_setInpError = _swmm5.error_setInpError
# This file is compatible with both classic and new-style classes.

cvar = _swmm5.cvar

