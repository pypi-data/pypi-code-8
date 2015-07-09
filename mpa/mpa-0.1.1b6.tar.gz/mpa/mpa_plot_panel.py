"""
MPA PLOT: SINGLE AXIS PROPERTIES
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""
#---------------------------------------------------
import mpa_proxy_modifier_axis        as MpaProxyModifierAxis 
import mpa_proxy_modifier_panel 	  as MpaProxyModifierPanel 
import mpa_proxy_modifier_legend      as MpaProxyModifierLegend  
import mpa_proxy_modifier_color_bar      as MpaProxyModifierColorBar 
#---------------------------------------------------

def refine_all_figure_panels(object_figure, list_axis_objects, 
	dict_plot_object_info_collector,
	dict_local_parameters):
	"""
	Refine the 
	:param object objec_figure: maplotlib Figure object 
	:param list list_axis_objects: list of matplotlib Axis objects 
	:param dict dict_legends: a python dict of legend parameters for all axes 
		with panel indices as keys and sub-dictionaries as values 
	:param dict dict_global_xy_minmax: a dictionary of global x/y min/max for each figure panel 
	:param dict dict_local_parameters: a python dict of local plot parameters with panel indices as keys
		and sub-dictionaries as values
	"""
	dict_legends = dict_plot_object_info_collector["LINE"]["dict_legends"]
	dict_global_xy_minmax = dict_plot_object_info_collector["LINE"]["dict_global_xy_minmax"]
	dict_color_bars = dict_plot_object_info_collector["MATRIX"]["dict_color_bar"]

	for panel_indices, dict_panel_parameters in dict_local_parameters.items():
		i_row, i_column = panel_indices
		object_axis = list_axis_objects[i_row, i_column]

		# Legend ON/OFF
		if dict_legends is None:
			isPanelLegendOn = False
		elif panel_indices in dict_legends.keys():
			isPanelLegendOn = dict_local_parameters[panel_indices]["legend_on"]
			dict_legend_for_current_panel = dict_legends[panel_indices]
		else:
			isPanelLegendOn = False

		# Color bar ON/OFF
		if dict_color_bars is None:
			isColorBarOn = False
		elif panel_indices in dict_color_bars.keys():
			isColorBarOn = dict_local_parameters[panel_indices]["color_bar_on"]
			dict_color_bar_for_current_panel = dict_color_bars[panel_indices]
		else:
			isColorBarOn = False

		#----------------------------------------------------------------------------------------------
		# Refine axis limits
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.set_user_defined_axis_limits(object_axis, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# Add figure panel label
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierPanel.add_figure_panel_labels(object_axis, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# Add axis label
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.set_axis_label(object_axis, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# Add legends
		#----------------------------------------------------------------------------------------------
		if isPanelLegendOn:
			MpaProxyModifierLegend.add_legend(dict_legend_for_current_panel, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# Add color bars
		#----------------------------------------------------------------------------------------------
		if isColorBarOn:
			MpaProxyModifierColorBar.add_color_bar(dict_color_bar_for_current_panel, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# Make axis limits tight
		#----------------------------------------------------------------------------------------------
		if dict_panel_parameters["x_limit_tight_on"]:
			new_min = dict_global_xy_minmax[panel_indices]['x']['min']
			new_max = dict_global_xy_minmax[panel_indices]['x']['max']
			print("New X min: {0}  max: {1}".format(new_min, new_max))
			MpaProxyModifierAxis.make_panel_axis_limit_tight(object_axis, 'x', new_min, new_max)

		if dict_panel_parameters["y_limit_tight_on"]:
			new_min = dict_global_xy_minmax[panel_indices]['y']['min']
			new_max = dict_global_xy_minmax[panel_indices]['y']['max']
			print("New Y min: {0}  max: {1}".format(new_min, new_max))
			MpaProxyModifierAxis.make_panel_axis_limit_tight(object_axis, 'y', new_min, new_max)
		

		#----------------------------------------------------------------------------------------------
		# Remove overlapping tick labels
		#----------------------------------------------------------------------------------------------
		if dict_panel_parameters["x_tick_label_hide_overlap"]:
			hide_first_how_many = dict_panel_parameters["x_tick_label_hide_first"]
			hide_last_how_many = dict_panel_parameters["x_tick_label_hide_last"]
			MpaProxyModifierAxis.hide_tick_label_overlap(object_axis, 'x', 
				hide_first_how_many, 
				hide_last_how_many,
				dict_panel_parameters)		
		if dict_panel_parameters["y_tick_label_hide_overlap"]:
			hide_first_how_many = dict_panel_parameters["y_tick_label_hide_first"]
			hide_last_how_many = dict_panel_parameters["y_tick_label_hide_last"]
			MpaProxyModifierAxis.hide_tick_label_overlap(object_axis, 'y', 
				hide_first_how_many, 
				hide_last_how_many,
				dict_panel_parameters)
		
		#----------------------------------------------------------------------------------------------
		# Refine the figure ticks
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.refine_ticks(object_axis, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# set user defined tick labels
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.set_tick_labels(object_axis, dict_panel_parameters)


		#----------------------------------------------------------------------------------------------
		# set user defined tick labels
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.set_ticks(object_axis, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# Rotate tick labels
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.rotate_tick_labels(object_axis, dict_panel_parameters)
		
		#----------------------------------------------------------------------------------------------
		# Add grid
		#----------------------------------------------------------------------------------------------
		if dict_panel_parameters["grid_on"]:
			MpaProxyModifierAxis.add_grid(object_figure, object_axis, dict_panel_parameters)	

			
		#----------------------------------------------------------------------------------------------
		# Set axis spine color
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.set_spine_color(object_axis, dict_panel_parameters)
			
		#----------------------------------------------------------------------------------------------
		# Set axis spine line width
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.set_spine_line_width(object_axis, dict_panel_parameters)

		#----------------------------------------------------------------------------------------------
		# Invert X/Y axis
		#----------------------------------------------------------------------------------------------
		if dict_panel_parameters["x_axis_inverted"]:
			MpaProxyModifierAxis.invert_axis('x', object_axis)
		elif dict_panel_parameters["y_axis_inverted"]:
			MpaProxyModifierAxis.invert_axis('y', object_axis)
		
		#----------------------------------------------------------------------------------------------
		# Hide axes
		#----------------------------------------------------------------------------------------------
		MpaProxyModifierAxis.set_axis_off(object_axis, dict_panel_parameters)