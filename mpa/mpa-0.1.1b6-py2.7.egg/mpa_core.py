"""
MPA: MATPLOTLIB PLOTTING ASSISTANT
AUTHOR: YUHANG WANG
DATE: 06-24-2015
Usage: python mpa.py FILE_LIST-OF-INPUT-DATA-FILE-NAMES FILE_PLOT-PARAMETERS
"""
#================================================
# Use Python 3 compatibility
#================================================
from __future__ import print_function, division
#================================================
import matplotlib
import matplotlib.pyplot 
import sys
import re
import numpy 
import pyparsing
#------------------------------------------------
# MPA Internal modules
#------------------------------------------------
import mpa_core_io   as MPA_IO
import mpa_core_plot as MPA_PLOT
#================================================

def main(file_configuration, preview=False):
	"""
	Main entry for MPA 
	:param str file_configuration: file name for the configuration file 
	:param bool preview: True | False(default) which decide whether to show a
		preview of the figure 
	"""
	#-------------------------------------------------------------------
	# [1] Read inputs
	#-------------------------------------------------------------------
	[dict_data_parameters, dict_global_parameters, 
	 dict_local_parameters] = MPA_IO.read_config(file_configuration)
	#-------------------------------------------------------------------
	# [3] Plot
	#-------------------------------------------------------------------
	object_figure, list_axis_objects = MPA_PLOT.plot(dict_data_parameters, 
		dict_global_parameters,
		dict_local_parameters)

	#-----------------------------------------------------------------
	# [4] Save
	#-----------------------------------------------------------------
	MPA_IO.write_figure(object_figure, 
		dict_global_parameters["figure_output_file"],
		figure_dpi = dict_global_parameters["figure_dpi"],
		figure_padding = dict_global_parameters["figure_padding"],
		figure_transparent = dict_global_parameters["figure_transparent"],
		)
	
	#-----------------------------------------------------------------
	# [5] Preview?
	#-----------------------------------------------------------------
	if preview: matplotlib.pyplot.show()

	return (object_figure, list_axis_objects)


if __name__ == '__main__':
	ccc = 1
	file_configuration = sys.argv[ccc]
	ccc += 1
	file_plot_parameters = sys.argv[ccc]

	preview=True
	main(file_configuration, file_plot_parameters, preview)

	