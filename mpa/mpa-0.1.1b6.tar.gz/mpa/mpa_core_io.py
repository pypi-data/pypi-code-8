"""
MPA CORE: IO
AUTHOR: YUHANG WANG 
DATE: 06-24-2015
"""
#----------------------------------------------------
from __future__ import print_function, division
#----------------------------------------------------
import re
#----------------------------------------------------
import mpa_reader_data_parameter   as MpaDataParameterReader
import mpa_reader_global_parameter as MpaGlobalParameterReader
import mpa_reader_local_parameter  as MpaLocalParameterReader
import mpa_writer_figure 		   as MpaFigureWriter
from mpa_syntax_marker import InputSectionMarkers as MpaInputSectionMarker
from mpa_syntax_marker import CommentMarkers      as MpaCommentMarkers
from mpa_data_type_ConfigRecordParser import ConfigRecordParser as MPA_CLASS_ConfigRecordParser
#----------------------------------------------------


#----------------------------------------------------
#                     INPUT
#----------------------------------------------------

def read_config(file_configuration):
	"""
	Read a file containing a list of plot parameters 
	and put them into a python dictionary.
	:param str file_configuration: name of the input configuration file
	:return: (dict_data_parameters, dict_global_plot_parameters, dict_local_plot_parameters)
	"""
	print("======================================================")
	print("  Reading input configuration file")
	print("  File: {0}".format(file_configuration))
	print("======================================================")
	
	object_data_parameter_parser = MPA_CLASS_ConfigRecordParser()
	object_global_parameter_parser = MPA_CLASS_ConfigRecordParser()
	object_local_parameter_parser = MPA_CLASS_ConfigRecordParser()

	dict_section_markers = MpaInputSectionMarker.get_dict()
	dict_comment_markers = MpaCommentMarkers.get_dict()
	
	symbol_comment = dict_comment_markers["INLINE COMMENT"]
	regex_pattern_comment = re.compile(r"^{0}.*".format(symbol_comment))
	
    # Update parameters based on user's specifications
	with open(file_configuration, 'r') as IN:
		which_section = None
		local_list_data_parameters = []
		local_list_global_parameters = []
		local_list_local_parameters = []
		for line in IN:
			line = line.strip()
			if regex_pattern_comment.match(line): continue # skip comments
			if line == '': continue # skip empty lines

			if line == dict_section_markers["DATA PARAMETER BEGIN"]:
				which_section = "DATA"
				continue
			elif line == dict_section_markers["GLOBAL PARAMETER BEGIN"]:
				which_section = "GLOBAL"
				continue
			elif line == dict_section_markers["LOCAL PARAMETER BEGIN"]:
				which_section = "LOCAL"
				continue

			if which_section == "DATA":
				# file parameters
				object_data_parameter_parser.read(line)

			elif which_section == "GLOBAL": 
				# global parameters
				object_global_parameter_parser.read(line)

			elif which_section == "LOCAL":
				# local parameters
				object_local_parameter_parser.read(line)

			else: continue # skip comments

	# Purge reading buffer and add the last information read into the record 
	object_data_parameter_parser.purge_buffer()
	object_global_parameter_parser.purge_buffer()
	# object_local_parameter_parser.purge_buffer()

	# Read file parameters 
	tuple_data_parameters = object_data_parameter_parser.get_parameters()
	dict_data_parameters  = MpaDataParameterReader.read(tuple_data_parameters)

	# Read global parameters
	tuple_global_parameters = object_global_parameter_parser.get_parameters()
	dict_global_plot_parameters = MpaGlobalParameterReader.read(tuple_global_parameters)

	# Read local parameters 
	tuple_local_parameters = object_local_parameter_parser.get_parameters()
	dict_local_plot_parameters = MpaLocalParameterReader.read(tuple_local_parameters)

	if len(dict_data_parameters.keys()) == 0:
		msg = "ERROR HINT: YOU MUST SPECIFY AT LEAST ONE GROUP OF INPUT DATA PARAMETERS\n"
		raise UserWarning(msg)

	return (dict_data_parameters, dict_global_plot_parameters, dict_local_plot_parameters)

#----------------------------------------------------
#                     OUTPUT
#----------------------------------------------------
def write_figure(*arg, **kwargs):
	"""
	Proxy for figure image writer
	"""
	return MpaFigureWriter.write(*arg, **kwargs)