"""
MPA CORE: PARAMETERS 
AUTHOR: YUHANG WANG 
DATE: 06-24-2015
"""
#----------------------------------------------------
# Import parameters
#----------------------------------------------------
from mpa_parameter_data   import DataParameters 
from mpa_parameter_axis   import AxisParameters
from mpa_parameter_color  import ColorParameters
from mpa_parameter_figure import FigureParameters
from mpa_parameter_grid   import GridParameters
from mpa_parameter_legend import LegendParameters
from mpa_parameter_panel  import PanelParameters
from mpa_parameter_tick   import TickParameters
from mpa_parameter_dependency import ExternalDependencyParameters
from mpa_parameter_twin_axis  import TwinAxisParameters
from mpa_parameter_color_bar  import ColorBarParameters
#----------------------------------------------------

class UserDataParameters:
	"""
	Global parameters for the entire figure 
	"""
	_list_of_parameter_classes_ = [
			DataParameters,
			]

	def __init__(self):
		self._list_of_parameter_classes_ = UserDataParameters._list_of_parameter_classes_

		self._convention_ = {}
		self._default_ = {}

		# Fill up self._convention_ and self._default_
		for _class in self._list_of_parameter_classes_:
			dict_convention = getattr(_class, "get_convention")()
			dict_defaults   = getattr(_class, "get_default")()
			for key, value in dict_convention.items():
				self._convention_[key] = value

			for key, value in dict_defaults.items():
				self._default_[key] = value


	def get_convention(self):
		return self._convention_

	def get_default(self):
		return self._default_.copy()

	@staticmethod
	def get_list_parameter_classes():
		"""
		Get a list of incorporated parameter classes 
		"""
		return UserDataParameters._list_of_parameter_classes_


class GlobalParameters:
	"""
	Global parameters for the entire figure 
	"""
	_list_of_parameter_classes_ = [
			ExternalDependencyParameters,
			FigureParameters,
			TwinAxisParameters,
			ColorParameters,
			]

	def __init__(self):
		self._list_of_parameter_classes_ = GlobalParameters._list_of_parameter_classes_

		self._convention_ = {}
		self._default_ = {}

		# Fill up self._convention_ and self._default_
		for _class in self._list_of_parameter_classes_:
			dict_convention = getattr(_class, "get_convention")()
			dict_defaults   = getattr(_class, "get_default")()
			for key, value in dict_convention.items():
				self._convention_[key] = value

			for key, value in dict_defaults.items():
				self._default_[key] = value


	def get_convention(self):
		return self._convention_

	def get_default(self):
		return self._default_.copy()

	@staticmethod
	def get_list_parameter_classes():
		"""
		Get a list of incorporated parameter classes 
		"""
		return GlobalParameters._list_of_parameter_classes_


class LocalParameters:
	"""
	Local parameters for each figure panel 
	"""
	_list_of_parameter_classes_ = [
			PanelParameters,
			AxisParameters,
			LegendParameters,
			GridParameters,
			TickParameters,
			ColorBarParameters,
			]


	def __init__(self):
		self._list_of_parameter_classes_ = LocalParameters._list_of_parameter_classes_
		self._convention_ = {}
		self._default_ = {}

		# Fill up self._convention_ and self._default_
		for _class in self._list_of_parameter_classes_:
			dict_convention = getattr(_class, "get_convention")()
			dict_defaults   = getattr(_class, "get_default")()
			for key, value in dict_convention.items():
				self._convention_[key] = value

			for key, value in dict_defaults.items():
				self._default_[key] = value


	def get_convention(self):
		return self._convention_

	def get_default(self):
		return self._default_.copy()

	@staticmethod
	def get_list_parameter_classes():
		"""
		Get a list of incorporated parameter classes 
		"""
		return LocalParameters._list_of_parameter_classes_


class ParameterManager:
	_list_of_parameter_classes_ = dict()
	_list_of_parameter_classes_["DATA"] = UserDataParameters.get_list_parameter_classes()
	_list_of_parameter_classes_["GLOBAL"] = GlobalParameters.get_list_parameter_classes()
	_list_of_parameter_classes_["LOCAL"] = LocalParameters.get_list_parameter_classes()
	_list_of_parameter_categories_ = ["DATA", "GLOBAL", "LOCAL"]
	@staticmethod
	def show(parameter_type, file_output=None):
		lines = ""
		for category in ParameterManager._list_of_parameter_categories_:
			lines += "--===================================--\n"
			lines += "             [[{0}]]\n".format(category)
			lines += "--===================================--\n"
			for _class in ParameterManager._list_of_parameter_classes_[category]:
				dict_convention = getattr(_class, "get_convention")()
				dict_defaults   = getattr(_class, "get_default")()
				type_parameter  = getattr(_class, "get_description")()
				lines += "------------------------------------------------\n"
				lines += "--------    {0} -------\n".format(type_parameter)
				lines += "------------------------------------------------\n"
				for key_public in sorted(dict_convention.keys()):
					key_internal = dict_convention[key_public]
					default_value = dict_defaults[key_internal]
					if parameter_type == "public":
						key = key_public
					else:
						key = key_internal
					lines += "{0}: {1}\n".format(key, default_value)
				lines += '\n'

		if file_output is not None:
			OUT = open(file_output, 'w')
			OUT.write(lines)
			OUT.close()
		else:
			print(lines)


if __name__ == "__main__":
	file_public = "PUBLIC_PARAMETERS.txt"
	file_internal = "INTERNAL_PARAMETERS.txt"
	manager = ParameterManager()
	manager.show("public", file_public)
	manager.show("internal", file_internal)