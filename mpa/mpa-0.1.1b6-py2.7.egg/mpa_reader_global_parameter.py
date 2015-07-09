"""
MPA PLOT PARAMETER READER 
AUTHOR: YUHANG WANG 
DATE: 06-24-2015
"""
#--------------------------------------------------------
import mpa_toolkit as MpaTk
from mpa_syntax_marker  import ParameterSeparators as MpaParameterSeparators
from mpa_core_parameter import GlobalParameters    as MpaGlobalParameters
#--------------------------------------------------------

def read(list_parameters):
	"""
	Read global plot parameters
	:param list_parameters: a list/tuple of parameters  
	:return: a python dictionary 
	"""
	dict_global_parametes = dict()
	dict_parameter_separators = MpaParameterSeparators.get_dict()
	object_mpaGlobalParameters = MpaGlobalParameters()
	dict_mpaGlobalParameters = object_mpaGlobalParameters.get_convention()
	dict_convention = object_mpaGlobalParameters.get_convention()
	dict_default = object_mpaGlobalParameters.get_default()

	symbol_parameter_separator = dict_parameter_separators["PARAMETER SEPARATOR"]
	symbol_key_value_separator = dict_parameter_separators["KEY VALUE SEPARATOR"]

	for line in list_parameters:
		local_list = line.split(symbol_parameter_separator)
		local_dict = dict()
		for _item in local_list:
			key,value = _item.split(symbol_key_value_separator)
			key = key.strip()
			value = value.strip()

			# convert to 'raw string literal' to preserve LaTex formating
			value = r"{0}".format(value)

			# check whether string "value" can be converted to boolean
			local_dict[key]  = MpaTk.transform_string_to_python_data_type(value)

		# [1] set the defaults
		for key,value in dict_default.items():
			dict_global_parametes[key] = value 

		# [2] update
		for key,value in local_dict.items():
			if key in dict_convention.keys():
				key = dict_convention[key] # change to internal representation of the key
			else:
				print("WARNING: you have specified an unknown GLOBAL PARAMETER: \"{0}\"".format(key))
				continue
			dict_global_parametes[key] = value 

	return dict_global_parametes