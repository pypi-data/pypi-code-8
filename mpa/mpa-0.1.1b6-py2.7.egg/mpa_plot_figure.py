"""
MPA PLOT: CHANGE FIGURE PROPERTIES 
AUTHOR: YUHANG WANG
DATE: 06-26-2015
"""
#---------------------------------------------------
import mpa_proxy_modifier_figure as MpaProxyModifierFigure 
#---------------------------------------------------


def refine_figure(object_figure, list_axis_objects, dict_global_parameters):
	"""
	Refine properties for all axes 
	:param list list_axis_objects: list of axis objects 
	:param dict dict_global_parameters: plot parameter dictionary
	"""

	#----------------------------------------------------------------------------------------------
	# Add figure common axis labels
	#----------------------------------------------------------------------------------------------
	MpaProxyModifierFigure.add_figure_common_axis_labels(list_axis_objects, dict_global_parameters)

