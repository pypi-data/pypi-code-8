"""
MPA PROXY: LEGEND MODIFIER
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""
#---------------------------------------------------
import matplotlib.pyplot
#---------------------------------------------------
import mpa_modifier_legend as MpaModifierLegend 
#---------------------------------------------------


def add_legend(dict_legend, dict_panel_parameters):
	"""
	Add and refine the legends for a particular figure panel 
	:param dict dict_legend: a dictionary of legend information for one particular figure panel 
	:param dict dict_panel_parameters: a dictionary of plotting parameters 
	"""
	object_old_axis_object = matplotlib.pyplot.gca() # store the current axis object
	

	object_axis = dict_legend["object_axis"]
	list_line_objects = dict_legend["list_line_objects"]
	list_legend_labels = dict_legend["list_legend_labels"]
	legend_anchor_coordinate = dict_panel_parameters["legend_anchor_coordinate"]
	legend_number_of_columns = dict_panel_parameters["legend_number_of_columns"]

	# set new current axis
	matplotlib.pyplot.sca(object_axis)
	
	MpaModifierLegend.add_legend(list_line_objects, list_legend_labels, 
		use_round_legend_box = dict_panel_parameters["use_round_legend_box"], 
		legend_anchor_corner = dict_panel_parameters["legend_anchor_corner"],
		legend_anchor_coordinate = legend_anchor_coordinate,
		show_legend_frame = dict_panel_parameters["show_legend_frame"],
		legend_frame_opacity = dict_panel_parameters["legend_frame_opacity"],
		legend_number_of_columns = legend_number_of_columns,
		legend_font_size = dict_panel_parameters["legend_font_size"],
		legend_font_weight = dict_panel_parameters["legend_font_weight"],
		legend_line_width = dict_panel_parameters["legend_line_width"],
		legend_marker_scale = dict_panel_parameters["legend_marker_scale"],
		legend_number_of_marker_points = dict_panel_parameters["legend_number_of_marker_points"],
		legend_number_of_scatter_marker_points = dict_panel_parameters["legend_number_of_marker_points"],
		legend_handle_length = dict_panel_parameters["legend_handle_length"],
		legend_border_padding = dict_panel_parameters["legend_border_padding"],
		legend_vertical_spacing = dict_panel_parameters["legend_vertical_spacing"],
		legend_padding_between_handle_and_text = dict_panel_parameters["legend_padding_between_handle_and_text"],
		legend_padding_between_border_and_axes = dict_panel_parameters["legend_padding_between_border_and_axes"],
		legend_column_spacing = dict_panel_parameters["legend_column_spacing"],
		legend_face_color = dict_panel_parameters["legend_face_color"],
		legend_edge_color = dict_panel_parameters["legend_edge_color"],
		)
	
	# reset current axis back to the original
	matplotlib.pyplot.sca(object_old_axis_object)