"""
MPA LEGEND PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""

class LegendParameters:
	"""
	Legend parameters
	"""
	_convention_ = {
		"LEGEND ON":"legend_on",
		"LEGEND ANCHOR COORDINATE":"legend_anchor_coordinate",
		"LEGEND NUMBER OF COLUMNS":"legend_number_of_columns",
		"LEGEND ANCHOR CORNER":"legend_anchor_corner",
		"LEGEND FRAME OPACITY":"legend_frame_opacity",
		"LEGEND FONT SIZE":"legend_font_size",
		"LEGEND FONT WEIGHT":"legend_font_weight",
		"LEGEND LINE WIDTH":"legend_line_width",
		"LEGEND MARKER SCALE":"legend_marker_scale",
		"LEGEND NUMBER OF MAKRER POINTS":"legend_number_of_marker_points",
		"LEGEND NUMBER OF SCATTER MAKRER POINTS":"legend_number_of_scatter_marker_points",
		"LEGEND HANDLE LENGTH":"legend_handle_length",
		"LEGEND BORDER PADDING":"legend_border_padding",
		"LEGEND VERTICAL SPACING":"legend_vertical_spacing",
		"LEGEND PADDING BETWEEN HANDLE AND TEXT":"legend_padding_between_handle_and_text",
		"LEGEND PADDING BETWEEN BORDER AND AXES":"legend_padding_between_border_and_axes",
		"LEGEND COLUMN SPACING":"legend_column_spacing",
		"LEGEND FACE COLOR":"legend_face_color",
		"LEGEND EDGE COLOR":"legend_edge_color",
		"LEGEND FACE OPACITY":"legend_face_opacity",
		"ROUND LEGEND BOX":"use_round_legend_box",
		"SHOW LEGEND FRAME":"show_legend_frame",
		"USE GLOBAL LEGEND":"use_global_legend",
		}

	_default_ = {
		"legend_on":False,
		"legend_anchor_coordinate": (0.9,0.9),
		"legend_number_of_columns":1,
		"legend_anchor_corner":"upper right",
		"legend_frame_opacity":0.5,
		"legend_font_size":26,
		"legend_font_weight":800,
		"legend_line_width":14,
		"legend_marker_scale":1,
		"legend_number_of_marker_points":None,
		"legend_number_of_scatter_marker_points":None,
		"legend_handle_length":2,
		"legend_border_padding":0.5,
		"legend_vertical_spacing":0.5,
		"legend_padding_between_handle_and_text":0.5,
		"legend_padding_between_border_and_axes":0,
		"legend_column_spacing":0.8,
		"legend_face_color":'w',
		"legend_edge_color":'k',
		"legend_face_opacity":1.0,
		"use_round_legend_box":True,
		"show_legend_frame":True,
		"use_global_legend":True,
		}

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return LegendParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return LegendParameters._default_.copy()

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "LEGEND PARAMETERS"