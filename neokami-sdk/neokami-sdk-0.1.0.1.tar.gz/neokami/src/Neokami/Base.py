''' Copyright 2015 Neokami GmbH. '''

from dicttoxml import dicttoxml

class Base():
	API_BASE = 'http://www.neokami.io'
	SDK_VERSION = '0.1'
	SDK_LANG = 'php'

	def getUrl(self, path):
		return self.API_BASE + path


	def toXML(self, array):
		return dicttoxml(array, attr_type=False)
