"""
MPA PLOT PROXY: FIGURE MODIFER 
AUTHOR: YUHANG WANG
DATE: 06-26-2015
"""
#------------------------------------------------------
import matplotlib.pyplot
#------------------------------------------------------
import mpa_modifier_axis as MpaModifierAxis 
#------------------------------------------------------

def add_figure_common_axis_labels(list_axis_objects, dict_global_parameters):
	"""
	Add the common X/Y axis labels and figure title 
	:param object list_axis_objects: a list of matplotlib Axis objects 
	:param dic dict_global_parameters: a python dict of global plot parameters 
		with keywords as keys and the user-defined/default values as values
	"""
	#----------------------------------------------------------
	# make an extra axis just to show the common X/Y label
	#----------------------------------------------------------
	object_extra_axis = list_axis_objects[-1, 0] # the extra axis is always the last one
	object_extra_axis.patch.set_alpha(0.)

	# turn off the extra axis's tick labels
	matplotlib.pyplot.setp(object_extra_axis.get_xticklabels(), visible=False)
	matplotlib.pyplot.setp(object_extra_axis.get_yticklabels(), visible=False)
	object_extra_axis.set_xticks([])
	object_extra_axis.set_yticks([])

	# Make the frame line transparent
	for child in object_extra_axis.get_children():
		if isinstance(child, matplotlib.spines.Spine):
			child.set_color((0,0,0,0))

	# Figure title
	if dict_global_parameters["figure_title"] is not None:
		MpaModifierFigure .add_title(object_extra_axis, dict_global_parameters["figure_title"], dict_global_parameters["figure_title_font_size"])

	#----------------------------------------------------------------------------------------------
	#	Axis Label
	#----------------------------------------------------------------------------------------------
	MpaModifierAxis.set_axis_label(object_extra_axis, 'x', 
		dict_global_parameters["figure_x_label"], 
		dict_global_parameters["figure_x_label_font_size"],
		dict_global_parameters["figure_x_label_padding"])
	MpaModifierAxis.set_axis_label(object_extra_axis, 'y', 
		dict_global_parameters["figure_y_label"], 
		dict_global_parameters["figure_y_label_font_size"],
		dict_global_parameters["figure_y_label_padding"])
	

