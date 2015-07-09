"""
MPA PLOT: create figure & axis objects
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""
#---------------------------------------------------------------
from __future__ import print_function, division
#---------------------------------------------------------------
import matplotlib.pyplot
import numpy
#---------------------------------------------------------------
import mpa_toolkit as MpaTool 
import mpa_modifier_panel as MpaModiferPanel 
#---------------------------------------------------------------

def figure(dict_global_plot_parameters, dict_local_plot_parameters):
	"""
	Create matplotlib figure & axis objects 
	:param dict dict_global_plot_parameters: an MPA dictionary of global plot parameters 
	:param dict dict_local_plot_parameters: an MPA dictionary of local plot parameters 
	:return: (object_figure, list_axis_objects)
	"""
	figureSize=(dict_global_plot_parameters["figure_length"], dict_global_plot_parameters["figure_height"])

	auto_adjust_returning_dimension = False
	object_figure, list_axis_objects = matplotlib.pyplot.subplots(
		nrows=dict_global_plot_parameters["figure_number_of_rows"],
		ncols=dict_global_plot_parameters["figure_number_of_columns"],
		figsize=figureSize,
		sharex=dict_global_plot_parameters["figure_share_x"],
		sharey=dict_global_plot_parameters["figure_share_y"],
		squeeze=auto_adjust_returning_dimension,
		)

	object_figure.subplots_adjust(hspace=dict_global_plot_parameters["figure_subplots_vertical_spacing"],
		wspace=dict_global_plot_parameters['figure_subplots_horizontal_spacing'])

	#----------------------------------
	# Create twin axis sharing x
	#----------------------------------
	if dict_global_plot_parameters["twinx_axis_source_index_list"] is not None:
		list_sources = dict_global_plot_parameters["twinx_axis_source_index_list"]
		if not MpaTool.is_multidimensional_list_tuple(list_sources):
			list_sources = [list_sources]
		
		for _index_pair in list_sources:
			id_row, id_column = _index_pair
			object_axis = list_axis_objects[id_row, id_column]
			new_axis_object = object_axis.twinx()
			
			# make a new 2D array matching the dimension of list_axis_objects
			n_rows, n_columns = numpy.shape(list_axis_objects)
			list_new_axis_objects = [new_axis_object]
			for i in range(n_columns-1): list_new_axis_objects.append(None)
			
			list_axis_objects = numpy.append(list_axis_objects,[list_new_axis_objects], axis=0)

	#----------------------------------
	# Create twin axis sharing y
	#----------------------------------
	if dict_global_plot_parameters["twiny_axis_source_index_list"] is not None:
		list_sources = dict_global_plot_parameters["twiny_axis_source_index_list"]
		if not MpaTool.is_multidimensional_list_tuple(list_sources):
			list_sources = [list_sources]
		
		for _index_pair in list_sources:
			id_row, id_column = _index_pair
			object_axis = list_axis_objects[id_row, id_column]
			new_axis_object = object_axis.twiny()
			
			# make a new 2D array matching the dimension of list_axis_objects
			n_rows, n_columns = numpy.shape(list_axis_objects)
			list_new_axis_objects = [new_axis_object]

			for i in range(n_columns-1): list_new_axis_objects.append(None)
			list_axis_objects = numpy.append(list_axis_objects,[list_new_axis_objects], axis=0)


	#----------------------------------
	# Add subdivision for some figure panels
	#----------------------------------
	for _, dict_panel in dict_local_plot_parameters.items():
		if dict_panel["panel_subdivision_on"]:
			id_row, id_column = dict_panel["panel_indices"]
			object_axis = list_axis_objects[id_row, id_column]
			new_object_axis = MpaModiferPanel.add_subdivision(object_axis, 
				dict_panel["panel_subdivision_location"],
				dict_panel["panel_subdivision_size"],
				dict_panel["panel_subdivision_padding"])
			list_new_axis_objects = [new_object_axis]
			# append None to keep the number of columns matching the list_axis_objects 
			for i in range(dict_global_plot_parameters["figure_number_of_columns"]-1): 
				list_new_axis_objects.append(None)
			list_axis_objects = numpy.append(list_axis_objects,[list_new_axis_objects], axis=0)


	#---------------------------------------------------
	# Add a global dummy axis (for global common X/Y labels)
	#---------------------------------------------------
	object_extra_axis = object_figure.add_subplot(1,1,1)
	n_rows, n_columns = numpy.shape(list_axis_objects)
	list_new_axis_objects = [object_extra_axis]
	
	# append None to keep the number of columns matching the list_axis_objects 
	for i in range(n_columns-1): list_new_axis_objects.append(None)
	
	list_axis_objects = numpy.append(list_axis_objects,[list_new_axis_objects], axis=0)

	#---------------------------------------------------
	# update the number of axis rows and columns
	#---------------------------------------------------
	n_rows, n_columns = numpy.shape(list_axis_objects)
	dict_global_plot_parameters["figure_number_of_rows"] = n_rows
	dict_global_plot_parameters["figure_number_of_columns"] = n_columns

	return (object_figure, list_axis_objects, dict_global_plot_parameters)
