"""
MPA PLOT PROXY: PANEL PROPERTY MODIFIER 
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""
#----------------------------------------------
import matplotlib.pyplot 
#----------------------------------------------
import mpa_modifier_panel   as MpaModifierPanel
import mpa_toolkit 			as MpaTk
#----------------------------------------------

def add_figure_panel_labels(object_axis, dict_plot_parameters):
	"""
	Proxy for adding figure panel labels 
	:param object object_axis: matplotlib Axis object 
	:param dict dict_plot_parameters: python dictionary of plotting parameters 

	"""
	object_old_axis_object = matplotlib.pyplot.gca() # store the current axis object
	
	if dict_plot_parameters["panel_label"] is None: return

	total_number_of_labels = len(dict_plot_parameters["panel_label"])
	for i in range(total_number_of_labels):
		if dict_plot_parameters["panel_label"][i] is not None:
			panel_label = MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label"], i)

			# A nice trick to allow user to input white space directly is to use list
			if isinstance(panel_label, list): panel_label = " ".join(panel_label) 

			# check whether the panel_label_box_anchor_coordinate is a list of number of list of lists
			if isinstance(dict_plot_parameters["panel_label_box_anchor_coordinate"][0], (int, long, float)):
				[x, y] = dict_plot_parameters["panel_label_box_anchor_coordinate"]
			else:
				[x, y] = MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_anchor_coordinate"], i)

		 	MpaModifierPanel.add_panel_label(object_axis, x, y, 
		 		panel_label,
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_font_size"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_horizontal_alignment"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_vertical_alignment"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_face_color"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_edge_color"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_opacity"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_padding"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_line_width"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_line_style"], i),
				MpaTk.get_array_item_i_safely(dict_plot_parameters["panel_label_box_shape"], i),
				)
	# reset current active axis
	matplotlib.pyplot.sca(object_old_axis_object)

def add_figure_panel_color_bar(object_axis, dict_plot_parameters):
	"""
	Add color bar to a figure panel 
	:param object object_axis: matplotlib Axis object 
	:param dict dict_plot_parameters: python dictionary of plotting parameters 
	"""
	MpaModifierPanel.add_panel_color_bar(object_axis,
		dict_plot_parameters["panel"])