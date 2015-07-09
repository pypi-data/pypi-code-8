"""
MPA SYNTAX MARKER CONVENTIONS
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""


class InputSectionMarkers:
	"""
	Configuration file section markers 
	"""
	_conventions_ = {
		"DATA PARAMETER BEGIN":"[[DATA]]",
		"GLOBAL PARAMETER BEGIN":"[[GLOBAL]]",
		"LOCAL PARAMETER BEGIN":"[[LOCAL]]",
	}

	@staticmethod
	def get_dict():
		return InputSectionMarkers._conventions_.copy()

class CommentMarkers:
	"""
	Configuration file comment markers 
	"""
	_conventions_ = {
		"INLINE COMMENT":"--",
	}

	@staticmethod
	def get_dict():
		return CommentMarkers._conventions_.copy()

class ScopeMarkers:
	"""
	Configuration file scope ending markers 
	i.e., markers that mark the end of the setup for one particular entity
	e.g., the parameters for one particular figure panel.
	"""
	_conventions_ = {
		"SCOPE END":"==="
	}

	@staticmethod
	def get_dict():
		return ScopeMarkers._conventions_.copy()

class ParameterSeparators:
	"""
	Configuration file parameter separators 
	"""
	_conventions_ = {
		"PARAMETER SEPARATOR":';',
		"KEY VALUE SEPARATOR":'::',
	}

	@staticmethod
	def get_dict():
		return ParameterSeparators._conventions_.copy()