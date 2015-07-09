"""
MPA PLOT: LINE
AUTHOR: YUHANG WANG
DATE: 07-03-2015
"""

#---------------------------------------------------------------
from __future__ import print_function, division
#---------------------------------------------------------------
import numpy
import matplotlib.pyplot 
#-----------------------------------------------
from mpa_data_type_InfoCollector import InfoCollector as MPA_CLASS_InfoCollector
import mpa_toolkit                   as MpaTool 
#---------------------------------------------------------------
def get_global_xy_minmax(list_data_keys, dict_data_parameters, dict_global_parameters):
	"""
	Get the global min/max for X/Y 
	:param list list_data_keys: dictionary keys for items to be plotted in dict_data_parameters
	:param dict dict_data_parameters: a dictionary of user data parameters 
	:param dict dict_global_parameters: a dictionary of global plot parameters 
	:return: dict_global_xy_minmax
		exampel usage: data_x_min = dict_global_xy_minmax[(0,0)]['x']["min"]
	"""
	#----------------------------------------------------------------------------------------------
	# make a 2D array to store the global min/max for each figure axis
	#----------------------------------------------------------------------------------------------
	n_rows = dict_global_parameters["figure_number_of_rows"]
	n_columns = dict_global_parameters["figure_number_of_columns"]

	dict_global_xy_minmax = dict()
	for i_row in range(n_rows):
		for i_column in range(n_columns):
			panel_indices = (i_row,i_column)
			dict_global_xy_minmax[panel_indices] = dict()
			dict_global_xy_minmax[panel_indices]['x'] = dict()
			dict_global_xy_minmax[panel_indices]['y'] = dict()
			dict_global_xy_minmax[panel_indices]['x']["min"] = None
			dict_global_xy_minmax[panel_indices]['x']["max"] = None			
			dict_global_xy_minmax[panel_indices]['y']["min"] = None
			dict_global_xy_minmax[panel_indices]['y']["max"] = None

	for _key in list_data_keys: # preserve the order of the input data files
		dict_data = dict_data_parameters[_key]
		user_data   = dict_data["data_value"]
		tuple_panel_indices = dict_data["data_panel_indices"]

		# Get X & Y from user_data
		data_X = user_data[:,0]
		data_Y = user_data[:,1]

		# update global min/max along X
		data_x_min = numpy.amin(data_X)
		data_x_max = numpy.amax(data_X)
		data_y_min = numpy.amin(data_Y)
		data_y_max = numpy.amax(data_Y)

		# update global x/y min/max
		dict_global_xy_minmax[tuple_panel_indices]['x']['min'] = MpaTool.return_smaller(
			dict_global_xy_minmax[tuple_panel_indices]['x']['min'], data_x_min)

		dict_global_xy_minmax[tuple_panel_indices]['x']['max'] = MpaTool.return_bigger(
			dict_global_xy_minmax[tuple_panel_indices]['x']['max'], data_x_max)

		dict_global_xy_minmax[tuple_panel_indices]['y']['min'] = MpaTool.return_smaller(
			dict_global_xy_minmax[tuple_panel_indices]['y']['min'], data_y_min)

		dict_global_xy_minmax[tuple_panel_indices]['y']['max'] = MpaTool.return_bigger(
			dict_global_xy_minmax[tuple_panel_indices]['y']['max'], data_y_max)

	return dict_global_xy_minmax


def plot(list_data_keys, list_axis_objects, dict_data_parameters, dict_global_parameters):
	"""
	Plot line objects; optionally plot the block-average
	:param list list_data_keys: dictionary keys for items to be plotted in dict_data_parameters
	:param list list_axis_objects: list of matplotlib Axis objects 
	:param dict dict_data_parameters: a dictionary of user data parameters 
	:param dict dict_global_parameters: a dictionary of global plot parameters
	:return: (dict_legends, dict_global_xy_minmax) 
	Example usage: 
		object_axis = dict_legends[(0,1)]["objec_axis"]
		data_x_min = dict_global_xy_minmax[(0,0)]['x']["min"]
	"""
	
	#----------------------------------------------------------------------------------------------
	# Create a PanelDB object to store all panel information
	#----------------------------------------------------------------------------------------------
	object_legendInfoCollector = MPA_CLASS_InfoCollector()

	#----------------------------------------------------------------------------------------------
	# ========= *** Start Plotting!  *** ================
	#----------------------------------------------------------------------------------------------
	ccc = 0
	# set line color
	list_global_color_order = dict_global_parameters["color_order"]
	dict_line_color_counter = dict()
	
	for _key in list_data_keys: 
		dict_data = dict_data_parameters[_key]
		tuple_panel_indices = dict_data["data_panel_indices"]
		user_data   = dict_data["data_value"]
		panel_id_row, _panel_id_column = tuple_panel_indices
		object_axis_for_panel = list_axis_objects[panel_id_row, _panel_id_column]


		#-------------------------------------------------
		# skip dummy axis objects
		#-------------------------------------------------
		if object_axis_for_panel is None: 
			print("skip", tuple_panel_indices)
			continue

		#-------------------------------------------------
		# Get X & Y from user_data
		#-------------------------------------------------
		data_X = user_data[:,0]
		data_Y = user_data[:,1]

		#-------------------------------------------------
		# update line color counter 
		#-------------------------------------------------
		if tuple_panel_indices not in dict_line_color_counter.keys():
			dict_line_color_counter[tuple_panel_indices] = 0
		else:
			dict_line_color_counter[tuple_panel_indices] += 1

		if dict_data["data_line_color"] is None:
			data_line_color = list_global_color_order[dict_line_color_counter[tuple_panel_indices]%len(list_global_color_order)]
		else:
			data_line_color = dict_data["data_line_color"]

		

		#-------------------------------------------------
		# Set the current active Axes instance to this axis 
		#-------------------------------------------------
		matplotlib.pyplot.sca(object_axis_for_panel)

		#-------------------------------------------------
		#  Plot!
		#-------------------------------------------------
		object_line, = object_axis_for_panel.plot(data_X,data_Y, 
			color=data_line_color,
			alpha=dict_data["data_line_opacity"],
			linestyle=dict_data["data_line_style"],
			)

		#-------------------------------------------------------------
		# Also plot the noise-filtered-averaged line
		#-------------------------------------------------------------
		if dict_data["data_show_block_average"]:
			from scipy import ndimage
			Y_block_averaged = ndimage.filters.uniform_filter(data_Y, 
				size=dict_data["data_block_average_block_size"], 
				mode="nearest")
			object_line, = object_axis_for_panel.plot(data_X,Y_block_averaged,
				linewidth=dict_data["data_block_average_line_width"],
				color=data_line_color,
				)

		#-------------------------------------------------------------
		# Add data legend information
		#-------------------------------------------------------------
		if dict_data["data_legend_on"]:
			tuple_legend_panel_indices = dict_data["data_legend_panel_indices"] # note: this can be different than tuple_panel_indices
			id_row_legend_panel, id_column_legend_panel = tuple_legend_panel_indices
			object_axis_for_legend = list_axis_objects[id_row_legend_panel, id_column_legend_panel]

			# axis object
			object_legendInfoCollector.set_item(tuple_legend_panel_indices, 
				"object_axis", object_axis_for_legend)
			
			# list of legend labels 
			object_legendInfoCollector.append_item(tuple_legend_panel_indices, 
				"list_legend_labels", dict_data["data_legend"])

			# list of line objects
			object_legendInfoCollector.append_item(tuple_legend_panel_indices,
				"list_line_objects", object_line)
		#-------------------------------------------------------------


		ccc += 1 # ==> continue to the next iteration
		#----------------------------------------------------------------------------------------------

	dict_legends = object_legendInfoCollector.get_dict()
	dict_global_xy_minmax = get_global_xy_minmax(list_data_keys, dict_data_parameters, dict_global_parameters)

	return (dict_legends, dict_global_xy_minmax)