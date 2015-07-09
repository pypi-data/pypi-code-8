"""
MPA COLOR BAR PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""


class ColorBarParameters:
	"""
	Color Bar Parameters
	"""
	_convention_ = {
		"COLOR BAR ON":"color_bar_on",
		"COLOR BAR SIZE":"color_bar_size",
		"COLOR BAR LOCATION":"color_bar_location",
		"COLOR BAR PADDING":"color_bar_padding",
		"COLOR BAR TICK LABEL FONT SIZE":"color_bar_tick_label_font_size",
		"COLOR BAR TICK LABEL NUMBER OF DECIMAL PLACES":"color_bar_tick_label_number_of_decimal_places",
		"COLOR BAR TICK ARRAY":"color_bar_tick_array",
		"COLOR BAR TICK WIDTH":"color_bar_tick_width",
		"COLOR BAR TICK LENGTH":"color_bar_tick_length",
		"COLOR BAR TICK COLOR":"color_bar_tick_color",
		}

	_default_ = {
		"color_bar_on":False,
		"color_bar_size":0.3,
		"color_bar_location":"right",
		"color_bar_padding":0.3,
		"color_bar_tick_label_font_size":20,
		"color_bar_tick_label_number_of_decimal_places":None,
		"color_bar_tick_array":None,
		"color_bar_tick_width":2,
		"color_bar_tick_length":7,
		"color_bar_tick_color":'k',
		}

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return ColorBarParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return ColorBarParameters._default_.copy()

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "COLOR BAR PARAMETERS"