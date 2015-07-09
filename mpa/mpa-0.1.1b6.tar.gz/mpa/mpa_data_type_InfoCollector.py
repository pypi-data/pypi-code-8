"""
MPA DATA TYPE: "InfoCollector" 
AUTHOR: YUHANG WANG
DATE: 06-25-2015
"""

class InfoCollector:
	def __init__(self):
		self._panel_dict = dict()

	def set_item(self, tuple_panel_indices, item_key, item_value):
		"""
		Add a new (singleton) item 
		"""
		if tuple_panel_indices not in self._panel_dict.keys():
			# use tuple as the dictionary key
			self._panel_dict[tuple_panel_indices] = dict()

		# Only the first will be kept. Subsequent setup will be ignored
		if item_key not in self._panel_dict[tuple_panel_indices].keys():
			self._panel_dict[tuple_panel_indices][item_key] = item_value

		return

	def append_item(self, tuple_panel_indices, item_key, item_value):
		"""
		Append an item to the existing list.
		If this is the first item in the list, a new list will be created.
		"""
		if tuple_panel_indices not in self._panel_dict.keys():
			# use tuple as the dictionary key
			self._panel_dict[tuple_panel_indices] = dict()

		# Create a new list if no existing one is found
		if item_key not in self._panel_dict[tuple_panel_indices].keys():
			self._panel_dict[tuple_panel_indices][item_key] = []

		self._panel_dict[tuple_panel_indices][item_key].append(item_value)

	def get_dict(self):
		"""
		Get a dictionary with all the information about all figure panels 
		"""
		return self._panel_dict.copy()
