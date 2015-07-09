"""
MPA AXIS GRID PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""


class GridParameters:
	"""
	Grid parameters 
	"""
	_convention_ = {
		"GRID ON":"grid_on",
		"GRID TICKS":"grid_ticks",
		"GRID AXIS":"grid_axis",
		"GRID LINE COLOR":"grid_line_color",
		"GRID LINE OPACITY":"grid_line_opacity",
		"GRID LINE WIDTH":"grid_line_width",
		"GRID LINE STYLE":"grid_line_style",
		"GRID Z ORDER":"grid_z_order",
		}

	_default_ = {
		"grid_on":False,
		"grid_ticks":"major",
		"grid_axis":"both",
		"grid_line_color":'k',
		"grid_line_opacity":0.2,
		"grid_line_width":1,
		"grid_line_style":'--',
		"grid_z_order":-1,
		}

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return GridParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return GridParameters._default_.copy()

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "GRID PARAMETERS"

