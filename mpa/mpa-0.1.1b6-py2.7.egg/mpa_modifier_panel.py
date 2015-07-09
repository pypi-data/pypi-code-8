"""
MPA PANEL MODIFIER
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""
#----------------------------------------------------
import matplotlib.pyplot
#----------------------------------------------------
import mpl_toolkits.axes_grid1 as MplTkAxes
#----------------------------------------------------

def add_panel_label(object_axis, x, y, 
			panel_label, 
			panel_label_font_size,
			panel_label_horizontal_alignment,
			panel_label_vertical_alignment,
			panel_box_face_color,
			panel_box_edge_color,
			panel_box_opacity,
			panel_box_padding,
			panel_box_line_width,
			panel_box_line_style,
			panel_box_shape,
			):
	"""
	Add a label to the panel 
	:param object object_axis: a matplotlib Axis object
	:param str panel_label: panel label (string)
	:param float x: x coordinate (0-1.0) with 0 for lower left and 1.0 for upper right
	:param float y: y coordinate (0-1.0) with 0 for lower left and 1.0 for upper right
	:param int panel_label_font_size: unit: points 
	:param int panel_label_font_weight: 0-1000
	:param str panel_label_horizontal_alignment: [ "center" | "right" | "left" ]
	:param str panel_label_vertical_alignment: [ "center" | "top" | "bottom" | "baseline" ]
	:param str panel_box_face_color: face color of the panel box (default: 'w'(i.e., white))
	:param str panel_box_edge_color: face color of the panel box (default: 'k'(i.e., black))
	:param float panel_box_opacity: 0-1.0
	:param int panel_box_padding: numerical value (default: 10)
	:param int panel_box_line_width: default: 4
	:param int panel_box_line_style: ["solid" | "dashed" | "dashdot" | "dotted"] default: "solid"
	:param str panel_box_shape: "square"(default) or "round"
	"""
	dict_font_properties = {
		"fontsize":panel_label_font_size,
		}
	dict_panel_box_properties = {
		"boxstyle":"{0},pad={1}".format(panel_box_shape, panel_box_padding),
		"facecolor":panel_box_face_color,
		"edgecolor":panel_box_edge_color,
		"alpha":panel_box_opacity,
		"linewidth":panel_box_line_width,
		"linestyle":panel_box_line_style,
		}
	object_axis.text(x,y, panel_label,
		fontdict=dict_font_properties,
		horizontalalignment=panel_label_horizontal_alignment,
		verticalalignment=panel_label_vertical_alignment,
		fontweight=0,
		transform=object_axis.transAxes, # use axis coordinate instead of the default data coordinate
		bbox=dict_panel_box_properties,
		)

def add_subdivision(object_axis, location, size, padding):
	"""
	Add a subdivision for a given figure panel 

	:param object object_axis: matplotlib Axes object 
	:param str location:  "top"| "bottom" | "left" | "right" 
	:param float size: size of the subdivision 
	:param float padding: padding between the new subdivision and the rest of the panel 
	"""
	object_axis_divider = MplTkAxes.make_axes_locatable(object_axis)
	object_axis = object_axis_divider.append_axes(location, 
		size=size, 
		pad=padding)
	return object_axis