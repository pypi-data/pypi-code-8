"""
MPA FIGURE AXIS PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""

class AxisParameters:
	"""
	Axis parameters 
	"""		
	_convention_ = {
		"AXIS OFF":"axis_off",
		"X LABEL":"x_label",
		"Y LABEL":"y_label",

		"X LABEL PADDING":"x_label_padding",
		"Y LABEL PADDING":"y_label_padding",

		"X LABEL FONT SIZE":"x_label_font_size",
		"Y LABEL FONT SIZE":"y_label_font_size",

		"X LIMIT USER DEFINED ON":"x_limit_user_defined_on",
		"Y LIMIT USER DEFINED ON":"y_limit_user_defined_on",
		"X LIMIT TIGHT ON":"x_limit_tight_on",
		"Y LIMIT TIGHT ON":"y_limit_tight_on",

		"X MIN":"x_min",
		"X MAX":"x_max",
		"Y MIN":"y_min",
		"Y MAX":"y_max",

		"X AXIS INVERTED":"x_axis_inverted",
		"Y AXIS INVERTED":"y_axis_inverted",

		"AXIS TOP SPINE COLOR":"axis_top_spine_color",
		"AXIS BOTTOM SPINE COLOR":"axis_bottom_spine_color",
		"AXIS LEFT SPINE COLOR":"axis_left_spine_color",
		"AXIS RIGHT SPINE COLOR":"axis_right_spine_color",

		"AXIS TOP SPINE LINE WIDTH":"axis_top_spine_line_width",
		"AXIS BOTTOM SPINE LINE WIDTH":"axis_bottom_spine_line_width",
		"AXIS LEFT SPINE LINE WIDTH":"axis_left_spine_line_width",
		"AXIS RIGHT SPINE LINE WIDTH":"axis_right_spine_line_width",

	}

	_default_ = {
		"axis_off":False,
		"x_label":None,
		"y_label":None,
		"x_label_padding":None,
		"y_label_padding":None,
		"x_label_font_size":40,
		"y_label_font_size":40,
		"x_limit_user_defined_on":False,
		"y_limit_user_defined_on":False,
		"x_limit_tight_on":False,
		"y_limit_tight_on":False,
		"x_min":None,
		"x_max":None,
		"y_min":None,
		"y_max":None,
		
		"x_axis_inverted":False,
		"y_axis_inverted":False,

		"axis_top_spine_color":None,
		"axis_bottom_spine_color":None,
		"axis_left_spine_color":None,
		"axis_right_spine_color":None,
		
		"axis_top_spine_line_width":None,
		"axis_bottom_spine_line_width":None,
		"axis_left_spine_line_width":None,
		"axis_right_spine_line_width":None,

		}

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return AxisParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return AxisParameters._default_.copy()

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "AXIS PARAMETERS"