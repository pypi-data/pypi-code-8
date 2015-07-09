"""
MPA COLOR BAR MODIFIER
AUTHOR: YUHANG WANG
DATE: 07-03-2015
"""
#----------------------------------------------------
import matplotlib.ticker 
import matplotlib.pyplot
#----------------------------------------------------
import mpl_toolkits.axes_grid1 as MplTkAxes
#----------------------------------------------------

def add_color_bar(object_axis,object_matrix_plot,
	bar_location="right",
	bar_size=1.0,
	bar_padding=0.3,
	bar_tick_label_font_size=20,
	bar_tick_label_number_of_decimal_places=None,
	bar_ticks=None,
	bar_tick_width=2,
	bar_tick_length=7,
	bar_tick_color='k'):
	"""
	Add color bar to an axis object 
	:param object object_axis: matplotlib Axis object 
	:parma object_matrix_plot: matplotlib Axis object returned  by matplotlib.pyplot.matshow()
	:parma str bar_location:  "top"| "bottom" | "left" | "right"  (default: "right")
	:param float bar_size:size of the color bar (default: 1.0)
	:param float bar_padding: padding between colorbar and its master axis(default: 0.3)
	:param int bar_tick_label_font_size: color bar tick label font size 
	:param int bar_tick_label_number_of_decimal_places: number of decimal places to show (default: None, i.e. use matplotlib default)
	:param list|tuple bar_ticks: a list/tuple of tick locations, e.g. (0, 0.5, 1.0) (default: None, i.e. use matplotlib default)
	"""
	#---------------------------------------
	# change tick number of decimal places
	# ref: http://stackoverflow.com/questions/25983218/scientific-notation-colorbar-in-matplotlib
	#---------------------------------------
	def tick_formatter(tick_value, tick_position):
			return "{0:.{1}f}".format(tick_value, bar_tick_label_number_of_decimal_places)

	object_axis_divider = MplTkAxes.make_axes_locatable(object_axis)
	object_axis_color_bar = object_axis_divider.append_axes(bar_location, 
		size=bar_size, 
		pad=bar_padding)

	if bar_tick_label_number_of_decimal_places is not None:
		object_color_bar = matplotlib.pyplot.colorbar(object_matrix_plot, 
			cax=object_axis_color_bar,
			ticks=bar_ticks,
			format=matplotlib.ticker.FuncFormatter(tick_formatter))
	else:
		object_color_bar = matplotlib.pyplot.colorbar(object_matrix_plot, 
			ticks=bar_ticks,
			cax=object_axis_color_bar)


	#---------------------------------------
	# change tick label font size
	#---------------------------------------
	for tick in object_color_bar.ax.get_yticklabels():
		tick.set_fontsize(bar_tick_label_font_size)

	#---------------------------------------
	# change tick thickness and length
	#---------------------------------------
	object_axis_color_bar.yaxis.set_tick_params(which="major", 
		width=bar_tick_width, 
		length=bar_tick_length, 
		color=bar_tick_color)



	
	return object_color_bar