"""
MPA FILE PARAMETER READER
AUTHOR: YUHANG WANG 
DATE: 06-25-2015
"""
#--------------------------------------------------------
import numpy
#--------------------------------------------------------
from mpa_syntax_marker  import ParameterSeparators as MpaParameterSeparators
from mpa_core_parameter import UserDataParameters  as MpaDataParameters
import mpa_toolkit as MpaTK 
#--------------------------------------------------------

def read(list_parameters):
	"""
	Read file parameters 
	:param list_parameters: a list/tuple of parameters 
	:return: a python dictionary of dictionaries 
	"""
	dict_data_parameters = dict()
	dict_parameter_separators = MpaParameterSeparators.get_dict()
	object_mpaDataParameters = MpaDataParameters()
	dict_convention = object_mpaDataParameters.get_convention()
	dict_defaults   = object_mpaDataParameters.get_default()

	symbol_parameter_separator = dict_parameter_separators["PARAMETER SEPARATOR"]
	symbol_key_value_separator = dict_parameter_separators["KEY VALUE SEPARATOR"]

	for i, line in enumerate(list_parameters):
		local_list = line.split(symbol_parameter_separator)
		local_dict = dict()
		for _item in local_list:
			print(_item)
			key,value = _item.split(symbol_key_value_separator)
			key = key.strip()
			value = value.strip()
			local_dict[key] = MpaTK.transform_string_to_python_data_type(value)

		file_name = local_dict["DATA FILE"]
		key_global = i
		dict_data_parameters[key_global] = dict()
		
		# [1] set the defaults
		for key_local,value in dict_defaults.items():
			dict_data_parameters[key_global][key_local] = value 
		
		# [2] update
		for key_local,value in local_dict.items():
			if key_local in dict_convention.keys():
				internal_key = dict_convention[key_local]
			else:
				print("WARNING: you have specified an unknown FILE PARAMETER: \"{0}\"".format(key))
				continue
			dict_data_parameters[key_global][internal_key] = value 

		# [3] add input data value
		dict_data_parameters[key_global]["data_value"] = numpy.loadtxt(file_name)

	return dict_data_parameters