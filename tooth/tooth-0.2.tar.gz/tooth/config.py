__author__ = 'Tom James Holub'

from ConfigParser import ConfigParser
import os.path


DEFAULT_PATH = None


def set_default_config_file_path(path):
	global DEFAULT_PATH
	DEFAULT_PATH = path


def get_default_config_file_path():
	global DEFAULT_PATH
	return DEFAULT_PATH


class Config():

	def __init__(self, path=None):
		path = path or get_default_config_file_path()
		if path is None:
			raise ValueError('Path not selected. Use Config(path=...) or config.set_default_config_file_path(...)')
		if not os.path.isfile(path):
			raise ValueError('No file found at %s' % path)

		self.config_parser = ConfigParser()
		self.config_parser.read(path)

	def get(self, section, name, value_type=str):
		value = self.config_parser.get(section, name)

		value = value.split('#')[0]
		value = value.strip(' \t')

		if section == 'path':
			if not os.path.exists(value):
				os.makedirs(value)
			return value

		if value == 'None':
			return None
		elif value_type == int:
			return int(value)
		elif value_type == bool:
			if value == 'True':
				return True
			elif value == 'False':
				return False
			else:
				raise ValueError('Cannot convert config value to bool, use either True or False. %s at %s:%s' % (value, section, name))
		elif value_type == list:
			return value.split(',')
		elif value_type == str:
			return value
		else:
			raise ValueError('value_type must be int, bool, str, list')