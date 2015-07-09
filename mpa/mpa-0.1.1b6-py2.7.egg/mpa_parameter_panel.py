"""
MPA FIGURE PANEL PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""


class PanelParameters:
	"""
	Panel Parameters
	"""
	_convention_ = {
		"PANEL INDICES":"panel_indices",
		"PANEL LABEL ON":"panel_label_on",
		"PANEL LABEL":"panel_label",
		"PANEL LABEL FONT SIZE":"panel_label_font_size",
		"PANEL LABEL HORIZONTAL ALIGNMENT":"panel_label_horizontal_alignment",
		"PANEL LABEL VERTICAL ALIGNMENT":"panel_label_vertical_alignment",
		"PANEL LABEL BOX FACE COLOR":"panel_label_box_face_color",
		"PANEL LABEL BOX EDGE COLOR":"panel_label_box_edge_color",
		"PANEL LABEL BOX OPACITY":"panel_label_box_opacity",
		"PANEL LABEL BOX PADDING":"panel_label_box_padding",
		"PANEL LABEL BOX LINE WIDTH":"panel_label_box_line_width",
		"PANEL LABEL BOX LINE STYLE":"panel_label_box_line_style",
		"PANEL LABEL BOX SHAPE":"panel_label_box_shape",
		"PANEL LABEL BOX ANCHOR COORDINATE":"panel_label_box_anchor_coordinate",
		"PANEL COLOR BAR ON":"panel_color_bar_on",
		"PANEL COLOR BAR SIZE":"panel_color_bar_size",
		"PANEL COLOR BAR LOCATION":"panel_color_bar_location",
		"PANEL COLOR BAR PADDING":"panel_color_bar_padding",
		"PANEL SUBDIVISION ON":"panel_subdivision_on",
		"PANEL SUBDIVISION LOCATION":"panel_subdivision_location",
		"PANEL SUBDIVISION SIZE":"panel_subdivision_size",
		"PANEL SUBDIVISION PADDING":"panel_subdivision_padding",
		}

	_default_ = {
		"panel_indices":None,
		"panel_label_on":False,
		"panel_label":None,
		"panel_label_font_size":25,
		"panel_label_horizontal_alignment":"left",
		"panel_label_vertical_alignment":"center",
		"panel_label_box_face_color":'w',
		"panel_label_box_edge_color":'w',
		"panel_label_box_opacity":0.8,
		"panel_label_box_padding":0.2,
		"panel_label_box_line_width":1,
		"panel_label_box_line_style":"solid",
		"panel_label_box_shape":"square",
		"panel_label_box_anchor_coordinate":(0.01,0.90),
		"panel_color_bar_on":False,
		"panel_color_bar_size":1.0,
		"panel_color_bar_location":"right",
		"panel_color_bar_padding":0.3,
		"panel_subdivision_on":False,
		"panel_subdivision_location":"right",
		"panel_subdivision_size":1.0,
		"panel_subdivision_padding":0.3,
		}

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return PanelParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return PanelParameters._default_.copy()

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "PANEL PARAMETERS"