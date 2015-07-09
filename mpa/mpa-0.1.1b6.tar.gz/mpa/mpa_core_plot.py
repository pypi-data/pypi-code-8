"""
MPA PLOT
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""
#---------------------------------------------------------------
from __future__ import print_function, division
#---------------------------------------------------------------
import matplotlib.pyplot
import numpy
#---------------------------------------------------------------
import mpa_plot_controller      as MpaPlotController 
import mpa_plot_create			as MpaPlotCreate 
import mpa_plot_panel			as MpaPlotPanel  
import mpa_plot_figure			as MpaPlotFigure 
#---------------------------------------------------------------


def plot(dict_data_parameters, dict_global_parameters, dict_local_parameters):
	"""
	Plot every data series in dict_data_parameters
	
	:param list dict_data_parameters: a list of dictionaries
	:param dict dict_global_parameters: a python dictionary of global plotting parameters
	:param dict dict_local_parameters: a python dictionary of local plotting parameters (per figure panel)
	:return: object for the current plot
	"""
	#-------------------------------------------------------------------
	# Manage external dependencies
	#-------------------------------------------------------------------
	#---------------------------------------------------
	#		Dependency: Latex
	#---------------------------------------------------
	if dict_global_parameters["use_latex"] is True:
		matplotlib.rcParams['text.usetex'] = True
		matplotlib.rcParams['text.latex.unicode'] = True
		matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']

	#-------------------------------------------------------------------
	# Create a list of figure/axis objects 
	#-------------------------------------------------------------------
	[object_figure, list_axis_objects, dict_global_parameters] = MpaPlotCreate.figure(dict_global_parameters,
		dict_local_parameters)
	
	#-------------------------------------------------------------------
	# Plot objects on the canvas
	#-------------------------------------------------------------------
	dict_plot_object_info_collector = MpaPlotController.plot(object_figure, 
					 							list_axis_objects,
												dict_data_parameters,
												dict_global_parameters)

	#----------------------------------------------------------------------------------------------
	# Refine properties for the entire figure
	#----------------------------------------------------------------------------------------------
	MpaPlotFigure.refine_figure(object_figure, list_axis_objects, dict_global_parameters)

	#----------------------------------------------------------------------------------------------
	# Refine properties per figure panel
	#----------------------------------------------------------------------------------------------
	MpaPlotPanel.refine_all_figure_panels(
		object_figure,
		list_axis_objects, 
		dict_plot_object_info_collector,
		dict_local_parameters)

	return (object_figure, list_axis_objects)
