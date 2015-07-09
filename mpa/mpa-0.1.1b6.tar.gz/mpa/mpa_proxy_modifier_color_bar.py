"""
MPA PROXY: COLOR BAR MODIFIER
AUTHOR: YUHANG WANG
DATE: 07-03-2015
"""
#---------------------------------------------------
import matplotlib.pyplot
#---------------------------------------------------
import mpa_modifier_color_bar as MpaModifierColorBar 
#---------------------------------------------------


def add_color_bar(dict_color_bar, dict_panel_parameters):
	"""
	Add and refine the legends for a particular figure panel 
	:param dict dict_color_bar: a dictionary of color bar information for one particular figure panel 
	:param dict dict_panel_parameters: a dictionary of plotting parameters 
	"""
	object_axis = dict_color_bar["object_axis"]
	object_matrix_plot = dict_color_bar["object_matrix_plot"]
	object_color_bar = MpaModifierColorBar.add_color_bar(object_axis,object_matrix_plot,
		bar_location = dict_panel_parameters["color_bar_location"],
		bar_size =  dict_panel_parameters["color_bar_size"],
		bar_padding = dict_panel_parameters["color_bar_padding"],
		bar_tick_label_font_size = dict_panel_parameters["color_bar_tick_label_font_size"],
		bar_tick_label_number_of_decimal_places = dict_panel_parameters["color_bar_tick_label_number_of_decimal_places"],
		bar_ticks = dict_panel_parameters["color_bar_tick_array"],
		bar_tick_width = dict_panel_parameters["color_bar_tick_width"],
		bar_tick_length = dict_panel_parameters["color_bar_tick_length"],
		bar_tick_color = dict_panel_parameters["color_bar_tick_color"],
		)

	return object_color_bar