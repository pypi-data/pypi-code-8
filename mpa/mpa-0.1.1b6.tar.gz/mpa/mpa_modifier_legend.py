"""
MPA LEGEND MODIFIER
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""
#----------------------------------------------------------
import matplotlib.pyplot
#----------------------------------------------------------

def add_legend(list_line_objects, list_legend_labels,
		use_round_legend_box,
		legend_anchor_corner, 
		legend_anchor_coordinate,
		show_legend_frame=None, 
		legend_frame_opacity=None,
		legend_number_of_columns=1,
		legend_font_size=10, 
		legend_font_weight=0,
		legend_line_width=1,
		legend_marker_scale=2,
		legend_number_of_marker_points=None,
		legend_number_of_scatter_marker_points=None,
		legend_handle_length=None,
		legend_border_padding=None,
		legend_vertical_spacing=None,
		legend_padding_between_handle_and_text=None,
		legend_padding_between_border_and_axes=None,
		legend_column_spacing=None,
		legend_face_color=None,
		legend_edge_color=None,
		):
	"""
	Add legend
	:param list list_line_objects: list of matplotlib Line object
	:param list list_legend_labels: list of legend labels
	:param use_round_legend_box: True or False to decide whether to use round legend box 
	:param legend_anchor_corner: i.e., "upper left" | "upper right" | "lower left" | "lower right" | "best"
	:param legend_anchor_coordinate: a tuple of two numbers between 0 and 1, e.g. (0.5, 0.5)
	:param bool show_legend_frame: True or False to decide whether to show legend box frame 
		(default: None, which will take value from legend.frameon rcParam)
	:param float legend_frame_opacity: a number between 0.0 and 1.0 
		(default: None, which means taking value from legend.framealpha rcParam)
	:param int number_legend_columns: number of legend columns (default: 1)
	:param int legend_font_size: font size for the legend
	:param int legend_font_weight: font weight (0-1000)
	:param int legend_line_width: line width for the legend 
	:param int legend_marker_scale: apply a scaling factor to the size of legend marker (relative to the original size)
			(default: 3)
	:param int legend_number_of_marker_points: number of marker samples in the legend 
			(default: None, i.e., use value from "legend.numpoints" in matplotlib's rcParam)	
	:param int legend_number_of_scatter_marker_points: number of marker samples in the legend for scatter plots
			(default: None, i.e., use value from "legend.scatterpoints" in matplotlib's rcParam)
	:param int legend_handle_length: unit: font-size unit 
			(default: None, i.e., use value from "legend.handlelength" in matplotlib's rcParam)
	:param float legend_border_padding: the whitespace between legend and the border in fractional float numbers  
			(default: None, i.e., use value from "legend.borderpad" in matplotlib's rcParam)
	:param float legend_vertical_spacing: the vertical spacing between legend entries (unit: fraction of the font-size )
			(default: None, i.e., use value from "legend.labelspacing" in matplotlib's rcParam)
	:param float legend_padding_between_handle_and_text: unit: fraction of the font size
			(default: None, i.e., use value from "legend.handletextpad" in matplotlib's rcParam)
	:param float legend_padding_between_border_and_axes: unit: fraction of the font-size 
			(default: None, i.e., use value from "legend.borderaxespad" in matplotlib's rcParam)
	:param float legend_column_spacing: spacing between columns; unit: fraction of the font-size
			(default: None, i.e., use value from "legend.columnspacing" in matplotlib's rcParam)
	:param float legend_face_color: legend face color (default: None, i.e., use matplotlib default)
	:param float legend_edge_color: legend edge color (default: None, i.e., use matplotlib default)
	"""
	matplotlib.pyplot.legend(list_line_objects, list_legend_labels,
		fancybox=use_round_legend_box,
		loc=legend_anchor_corner, 
		bbox_to_anchor=legend_anchor_coordinate,
		frameon=show_legend_frame,
		framealpha=legend_frame_opacity,
		ncol=legend_number_of_columns,
		fontsize=legend_font_size,
		markerscale=legend_marker_scale,
		numpoints=legend_number_of_marker_points,
		handlelength=legend_handle_length,
		borderpad=legend_border_padding,
		labelspacing=legend_vertical_spacing,
		handletextpad=legend_padding_between_handle_and_text,
		borderaxespad=legend_padding_between_border_and_axes,
		columnspacing=legend_column_spacing,
		)
	object_legend = matplotlib.pyplot.gca().get_legend()
	object_legend_lines = object_legend.get_lines() # get all the lines.Line2D instance from the legend
	object_legend_text  = object_legend.get_texts() # get all the text.Text instance from the legend
	matplotlib.pyplot.setp(object_legend_lines, linewidth=legend_line_width)
	matplotlib.pyplot.setp(object_legend_text, fontweight=legend_font_weight)

	# Change legend face color
	object_legend_frame = object_legend.get_frame() # get the patch.Rectangle instance surrounding the legend
	if legend_face_color is not None:
		object_legend_frame.set_facecolor(legend_face_color)	

	# Change legend edge color
	if legend_face_color is not None:
		object_legend_frame.set_edgecolor(legend_edge_color)	

	return object_legend
