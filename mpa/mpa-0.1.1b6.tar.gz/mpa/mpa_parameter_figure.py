"""
MPA FIGURE PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""

class FigureParameters:
	"""
	Figure parameters
	"""
	_convention_ = {
		"FIGURE OUTPUT FILE":"figure_output_file",
		"FIGURE TITLE":"figure_title",
		"FIGURE TITLE FONT SIZE":"figure_title_font_size",
		"FIGURE LENGTH":"figure_length",
		"FIGURE HEIGHT":"figure_height",
		"FIGURE NUMBER OF ROWS":"figure_number_of_rows",
		"FIGURE NUMBER OF COLUMNS":"figure_number_of_columns",
		"FIGURE SHARE X":"figure_share_x",
		"FIGURE SHARE Y":"figure_share_y",
		"FIGURE SUBPLOTS VERTICAL SPACING":"figure_subplots_vertical_spacing",
		"FIGURE SUBPLOTS HORIZONTAL SPACING":"figure_subplots_horizontal_spacing",
		"FIGURE DPI":"figure_dpi",
		"FIGURE TRANSPARENT":'figure_transparent',
		"FIGURE PADDING":"figure_padding",
		"FIGURE X LIMITS TIGHT":"figure_x_limits_tight",
		"FIGURE Y LIMITS TIGHT":"figure_y_limits_tight",
		"FIGURE X LIMITS USER DEFINED":"figure_x_limits_user_defined",
		"FIGURE Y LIMITS USER DEFINED":"figure_y_limits_user_defined",
		"FIGURE AXIS LABEL ON":"figure_axis_label_on",
		"FIGURE X LABEL":"figure_x_label",
		"FIGURE Y LABEL":"figure_y_label",
		"FIGURE X LABEL FONT SIZE":"figure_x_label_font_size",
		"FIGURE Y LABEL FONT SIZE":"figure_y_label_font_size",
		"FIGURE X LABEL PADDING":"figure_x_label_padding",
		"FIGURE Y LABEL PADDING":"figure_y_label_padding",
		}

	_default_ = {
		"figure_output_file":"output.png",
		"figure_title":None,
		"figure_title_font_size":40,
		"figure_length":12,
		"figure_height":8,
		"figure_number_of_rows":1,
		"figure_number_of_columns":1,
		"figure_share_x":"none",
		"figure_share_y":"none",
		"figure_subplots_vertical_spacing":None,
		"figure_subplots_horizontal_spacing":None,
		"figure_dpi":150,
		"figure_transparent":False,
		"figure_padding":0.2,
		"figure_x_limits_tight":True,
		"figure_y_limits_tight":False,
		"figure_x_limits_user_defined":False,
		"figure_y_limits_user_defined":False,
		"figure_axis_label_on":False,
		"figure_x_label":'',
		"figure_y_label":'',
		"figure_x_label_font_size":40,
		"figure_y_label_font_size":40,
		"figure_x_label_padding":60,
		"figure_y_label_padding":60,
		}

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return FigureParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return FigureParameters._default_.copy()

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "FIGURE PARAMETERS"

