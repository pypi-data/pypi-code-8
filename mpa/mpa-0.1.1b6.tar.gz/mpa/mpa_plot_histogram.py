"""
MPA PLOT: HISTOGRAM
AUTHOR: YUHANG WANG
DATE: 07-08-2015
"""
#---------------------------------------------------------------
from __future__ import print_function, division
#---------------------------------------------------------------
import numpy
import matplotlib.pyplot 
#-----------------------------------------------
import mpa_modifier_data   	as MpaModifierData  
from mpa_data_type_InfoCollector import InfoCollector as MPA_CLASS_InfoCollector
#---------------------------------------------------------------

def plot(list_data_keys, list_axis_objects, dict_data_parameters, dict_global_parameters):
	"""
	Plot histogram objects
	:param list list_data_keys: dictionary keys for items to be plotted in dict_data_parameters
	:param list list_axis_objects: list of matplotlib Axis objects 
	:param dict dict_data_parameters: a dictionary of user data parameters 
	:param dict dict_global_parameters: a dictionary of global plot parameters
	:return: dict_legends 
	Example usage: 
		object_axis = dict_legends[(0,1)]["objec_axis"]
		data_x_min = dict_global_xy_minmax[(0,0)]['x']["min"]
	"""
	#----------------------------------------------------------------------------------------------
	# Create a PanelDB object to store all panel information
	#----------------------------------------------------------------------------------------------
	object_LegendInfoCollector = MPA_CLASS_InfoCollector()

	#----------------------------------------------------------------------------------------------
	# ========= *** Start Plotting!  *** ================
	#----------------------------------------------------------------------------------------------
	for _key in list_data_keys: 
		dict_data = dict_data_parameters[_key]
		tuple_panel_indices = dict_data["data_panel_indices"]
		panel_id_row, _panel_id_column = tuple_panel_indices
		object_panel_axis = list_axis_objects[panel_id_row, _panel_id_column]

		#-------------------------------------------------
		# User data
		#-------------------------------------------------
		user_data = dict_data["data_value"]
		if dict_data["data_matrix_transpose"]:
			user_data = numpy.transpose(user_data)

		# skip dummy axis objects
		#-------------------------------------------------
		if object_panel_axis is None: 
			print("skip", tuple_panel_indices)
			continue

		#-------------------------------------------------
		# Set the current active Axes instance to this axis 
		#-------------------------------------------------
		matplotlib.pyplot.sca(object_panel_axis)

		#-------------------------------------------------
		#  Plot!
		#-------------------------------------------------
		print("panel: ", tuple_panel_indices)
		number_of_data_rows, number_of_data_columns = numpy.shape(user_data)
		object_matrix_plot = object_panel_axis.matshow(user_data,
			vmin=dict_data["data_matrix_vertical_min"],
			vmax=dict_data["data_matrix_vertical_max"])

		#-----------------------------------------------------------------------------
		# change matrix x/y extent
		#-----------------------------------------------------------------------------
		list_axis_extent = list(matplotlib.pyplot.getp(object_matrix_plot, "extent"))
		
		x_offset = dict_data["data_matrix_x_extent_offset"]
		y_offset = dict_data["data_matrix_y_extent_offset"]

		if dict_data["data_matrix_x_extent_min"] is not None:
			list_axis_extent[0] = dict_data["data_matrix_x_extent_min"] + x_offset
		if dict_data["data_matrix_x_extent_max"] is not None:
			list_axis_extent[1] = dict_data["data_matrix_x_extent_max"] + x_offset
		if dict_data["data_matrix_y_extent_min"] is not None:
			list_axis_extent[2] = dict_data["data_matrix_y_extent_min"] + y_offset
		if dict_data["data_matrix_y_extent_max"] is not None:
			list_axis_extent[3] = dict_data["data_matrix_y_extent_max"] + y_offset

		x_min, x_max, y_min, y_max = list_axis_extent
		MpaModifierData .set_matrix_extent(object_matrix_plot, x_min, x_max, y_min, y_max)

		#--------------------------------------------------------------------------------
		# change  aspect ratio to be automatically adjusted
		#--------------------------------------------------------------------------------
		object_panel_axis.set_aspect("auto", adjustable="box-forced", anchor="SW")
		
		#-------------------------------------------------
		# Collect color bar information
		#-------------------------------------------------
		if dict_data["data_matrix_color_bar_on"]:
			tuple_color_bar_panel_indices = dict_data["data_matrix_color_bar_panel_indices"] # note: this can be different than tuple_panel_indices
			id_row_legend_panel, id_column_legend_panel = tuple_color_bar_panel_indices
			object_axis_for_color_bar = list_axis_objects[id_row_legend_panel, id_column_legend_panel]

			# axis object
			object_LegendInfoCollector.set_item(tuple_color_bar_panel_indices, 
				"object_axis", object_axis_for_color_bar)

			# add object_matrix_plot
			object_LegendInfoCollector.set_item(tuple_color_bar_panel_indices,
				"object_matrix_plot", object_matrix_plot)
			

		dict_color_bars = object_LegendInfoCollector.get_dict()

	return dict_color_bars
