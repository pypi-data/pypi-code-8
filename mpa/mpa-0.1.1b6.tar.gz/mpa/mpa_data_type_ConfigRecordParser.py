"""
MPA DATA TYPE: "ConfigRecord" -- CONFIGURATION FILE RECORD
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""
#------------------------------------------------------------------------
import re
#------------------------------------------------------------------------
from mpa_syntax_marker import ScopeMarkers        as MpaScopeMarkers
#------------------------------------------------------------------------

class ConfigRecordParser:
	def __init__(self):
		self._list_parameters = []
		self._list_buffer = []
		dict_scope_markers = MpaScopeMarkers.get_dict()
		symbol_scope_end = dict_scope_markers["SCOPE END"]
		self.regex_pattern_scope_end = re.compile(r"^{0}$".format(symbol_scope_end))


	def read(self, input_string):
		"""
		Read an input string
		:param str input_string: input string 
		"""
		if self.regex_pattern_scope_end.match(input_string):
			if len(self._list_buffer) > 0:
				# convert list to a string
				line = ";".join(self._list_buffer)
				self._list_parameters.append(line)
				self._list_buffer = [] # reset
			else: return
		elif input_string != '':
			self._list_buffer.append(input_string)
		else:
			return 

	def get_parameters(self):
		"""
		Get the parameters 
		"""
		return tuple(self._list_parameters)

	def purge_buffer(self):
		"""
		Purge the current buffer
		"""
		if len(self._list_buffer) > 0:
			# convert list to a string
				line = ";".join(self._list_buffer)
				self._list_parameters.append(line)
				self._list_buffer = [] 
		return 
