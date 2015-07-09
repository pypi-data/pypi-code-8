"""
MPA PLOT: LINE 
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""
#-----------------------------------------------
import mpa_plot_line 	as MpaPlotLine 
import mpa_plot_matrix 	as MpaPlotMatrix 
import mpa_plot_histogram as MpaPlotHistogram 
#-----------------------------------------------
from mpa_data_type_InfoCollector import InfoCollector as MPA_CLASS_InfoCollector
#-----------------------------------------------

def plot(object_figure, 
	list_axis_objects, 
	dict_data_parameters,
	dict_global_parameters,
	):
	"""
	Plot line objects 
	:param object object_figure: a matplotlib Figure object 
	:param list list_axis_objects: list of matplotlib Axis objects 
	:param list dict_data_parameters: a dictionary of user data parameters 
		which file name as key and a dictionary as value
	:param dict dict_global_parameters: a dictionary of global plot parameters 

	"""
	#----------------------------------------------------------------------------------------------
	# Create a PanelDB object to store all newly generated information
	#----------------------------------------------------------------------------------------------
	object_plotObjectInfoCollector = MPA_CLASS_InfoCollector()

	#---------------------------------------------------
	#		Dependency: SciPy
	#---------------------------------------------------
	if dict_global_parameters["use_scipy"] is True:
		import scipy


	#---------------------------------------------------
	# Find the plot type for each data series
	#---------------------------------------------------
	dict_grouped_global_keys = dict()
	for _key in sorted(dict_data_parameters.keys()): # preserve the order of the input data files
		dict_data = dict_data_parameters[_key]
		plot_type = dict_data["data_plot_type"]
		if plot_type not in dict_grouped_global_keys.keys():
			dict_grouped_global_keys[plot_type] = []
		dict_grouped_global_keys[plot_type].append(_key)
	
	#---------------------------------------------------
	# Plot objects 
	#---------------------------------------------------
	dict_line_legends = None
	dict_line_global_xy_minmax = None
	dict_matrix_color_bar = None
	dict_histogram_legends = None
	for _plot_type in dict_grouped_global_keys:
		_list_keys = dict_grouped_global_keys[_plot_type]
		if _plot_type == "line":
			[dict_line_legends, dict_line_global_xy_minmax] = MpaPlotLine.plot(_list_keys, list_axis_objects, dict_data_parameters, dict_global_parameters)

		elif _plot_type == "matrix":
			dict_matrix_color_bar = MpaPlotMatrix.plot(_list_keys, list_axis_objects, dict_data_parameters, dict_global_parameters)

		elif _plot_type == "histogram":
			dict_histogram_legends = MpaPlotHistogram.plot(_list_keys, list_axis_objects, dict_data_parameters, dict_global_parameters)

	object_plotObjectInfoCollector.set_item("LINE", "dict_legends", dict_line_legends)
	object_plotObjectInfoCollector.set_item("LINE", "dict_global_xy_minmax", dict_line_global_xy_minmax)
	object_plotObjectInfoCollector.set_item("MATRIX", "dict_color_bar", dict_matrix_color_bar)
	object_plotObjectInfoCollector.set_item("HISTOGRAM", "dict_legends", dict_matrix_color_bar)

	return object_plotObjectInfoCollector.get_dict()