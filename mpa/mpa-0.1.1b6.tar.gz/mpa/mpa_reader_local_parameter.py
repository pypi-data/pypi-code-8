"""
MPA LOCAL PARAMETER READER
AUTHOR: YUHANG WANG 
DATE: 06-25-2015
"""
#--------------------------------------------------------
import mpa_toolkit as MpaTk 
from mpa_syntax_marker  import ParameterSeparators as MpaParameterSeparators
from mpa_core_parameter import LocalParameters     as MpaLocalParameters
#--------------------------------------------------------

def read(list_parameters):
	"""
	Read local plot parameters 
	:param list_parameters: a list/tuple of parameters 
	:return: a python dictionary of dictionaries 
	"""
	dict_local_parametes = dict()
	dict_parameter_separators = MpaParameterSeparators.get_dict()

	object_mpaLocalParameters = MpaLocalParameters()
	dict_convention = object_mpaLocalParameters.get_convention()
	dict_defaults   = object_mpaLocalParameters.get_default()

	symbol_parameter_separator = dict_parameter_separators["PARAMETER SEPARATOR"]
	symbol_key_value_separator = dict_parameter_separators["KEY VALUE SEPARATOR"]

	for line in list_parameters:
		local_list = line.split(symbol_parameter_separator)
		local_dict = dict()
		for _item in local_list:
			key,value = _item.split(symbol_key_value_separator)
			key = key.strip()
			value = value.strip()
			local_dict[key] = MpaTk.transform_string_to_python_data_type(value)

		if "PANEL INDICES" not in local_dict.keys():
			msg = "ERROR HINT: each local parameter section must have \"PANEL INDICES\" specified "
			raise UserWarning(msg)
			
		panle_indices = local_dict["PANEL INDICES"]
		key_global = panle_indices
		dict_local_parametes[panle_indices] = dict()
		
		# [1] set the defaults
		for key_local,value in dict_defaults.items():
			dict_local_parametes[key_global][key_local] = value 
		
		# [2] update
		for key_local,value in local_dict.items():
			if key_local in dict_convention.keys():
				key_local = dict_convention[key_local] # convert to internal representation of the key
			else:
				print("WARNING: you have specified an unknown LOCAL PARAMETER: \"{0}\"".format(key_local))
				continue
			dict_local_parametes[key_global][key_local] = value 

	return dict_local_parametes