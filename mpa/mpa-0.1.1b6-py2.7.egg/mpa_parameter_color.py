"""
MPA COLOR PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""


class ColorParameters:
	"""
	Color parameters 
	"""
	_convention_ = {
		"COLOR ORDER":"color_order",
		}

	_default_ = {
		"color_order":['k','r','g','b','m','y','c'],
		}

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return ColorParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return ColorParameters._default_.copy()

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "COLOR PARAMETERS"
